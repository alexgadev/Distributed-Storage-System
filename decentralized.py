import os
import yaml 
import grpc
import time
import random
from concurrent import futures
from proto import store_pb2, store_pb2_grpc

class DecentralizedStorageSystem(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, addr, weight, neighbor):
        self.address = addr
        self.weight = weight
        
        self.storage = {}
        self.delay = 0
        self.slowed = False
        self.weight_for_reads = 2
        self.weight_for_writes = 3

        self.nodes = {}

        self.consistency_file = f"decentralized_recovery_file.txt"
        self.recover_from_failure(self.consistency_file)

        try:
            neigh_address = f"{neighbor['ip']:{neighbor['port']}}"
            channel = grpc.insecure_channel(neigh_address)
            stub = store_pb2_grpc.KeyValueStoreStub(channel=channel)

            stub.registerNode(store_pb2.RegisterRequest(address=neigh_address, weight=neighbor['weight']))
            self.nodes[neigh_address] = stub, weight      
        except Exception as e:
            exit() # means this node is likely to be isolated and that wouldn't be a nice cluster
        
        
    def registerNode(self, request, context):
        weight = request.weight
        if request.address not in self.nodes:
            channel = grpc.insecure_channel(request.address)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)

            self.nodes[request.address] = stub, weight
        else:
            stub, weight = self.nodes.get(request.address)
        
        # obtain an address which isn't self nor request.address
        l = list(self.nodes.keys())
        i = 0
        while l[i] == self.address or l[i] == request.address and i < len(l):
            address = l[i]
            i += 1
        
        if address in list(self.nodes.keys()) or i >= len(l):
            address = None
        else:
            w = self.nodes[address]['weight']
            stub.gossip(store_pb2.GossipRequest(address=address, weight=w))

        return store_pb2.Empty()        

    def gossip(self, request, context):
        if request.address not in self.nodes:
            channel = grpc.insecure_channel(request.address)
            stub = store_pb2_grpc.KeyValueStoreStub(channel=channel)

            stub.registerNode(store_pb2.RegisterRequest(address=request.address, weight=request.w))
            self.nodes[request.address] = stub, request.w 
        return store_pb2.Empty()

    def recover_from_failure(self, file):
        try:
            with open(file, "r") as fp:
                for line in fp:
                    key, value = line.strip().split(':')
                    self.storage[key] = value
        except FileNotFoundError:
            pass

    def write_to_consistency_file(self, file, key, value):
        try:
            with open(file, "r") as fp:
                content = fp.readlines()
        except FileNotFoundError:
            with open(file, "w") as fp:
                fp.write(f"{key}:{value}\n")
        else:
            
            key_exists = False
            for i, line in enumerate(content):
                if key in line:
                    content[i] = f"{key}:{value}\n"
                    key_exists = True
                    break
            
            if not key_exists:
                content.append(f"{key}:{value}\n")
            
            with open(file, "w") as fp:
                fp.writelines(content)


    def put(self, request, context):
        if self.slowed:
            return store_pb2.PutResponse(success=False)
        else:
            key = request.key
            value = request.value
            quorum = self.weight
            
            for key, value in self.nodes.items():
                vote_request = store_pb2.VoteRequest(key=key)
                vote_response = value[0].canCommit(vote_request)
                if vote_response.vote:
                    quorum += value[1]
            
            if quorum >= self.weight_for_writes:
                commit_quorum = self.weight
                for pair in self.nodes.values():
                    commit_request = store_pb2.CommitRequest(key=key, value=value)
                    commit_response = pair[0].doCommit(commit_request)
                    if commit_response.committed:
                        commit_quorum += pair[1]

                if commit_quorum >= self.weight_for_writes:
                    self.storage[key] = value
                    self.write_to_consistency_file(self.consistency_file, key, value)
                    return store_pb2.PutResponse(success=True)
                else:
                    for pair in self.nodes.values():
                        req = store_pb2.AbortRequest(key=key)
                        pair[0].doAbort(req)
                    return store_pb2.PutResponse(success=False)
            else:
                return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        if self.slowed:
            return store_pb2.GetResponse(value=None, found=False)
        else:
            key = request.key
            value = request.value
            quorum_weights = {}

            quorum_weights[self.storage[key]] = self.weight            
            for key, value in self.nodes.items():
                vote_request = store_pb2.VoteRequest(key=key)
                vote_response = value[0].askVote(vote_request)
                if vote_response.vote:
                    quorum_weights[vote_response.value] += value[1]
                else:
                    quorum_weights[vote_response.value] = value[1]
            
            val = max(quorum_weights, key=lambda k: quorum_weights[k]) #TODO: change
            if quorum_weights[val] >= self.weight_for_reads:
                return store_pb2.GetResponse(value=val, found=True)
            else:
                return store_pb2.GetResponse(value=None, found=False)
        
    def slowDown(self, request, context):
        self.delay = request.seconds
        self.slowed = True
        while self.delay > 0:
            time.sleep(1)
            self.delay -= 1
        return store_pb2.SlowDownResponse(success=True)

    def restore(self, request, context):
        self.delay = 0
        self.slowed = False
        return store_pb2.RestoreResponse(success=True)

    def canCommit(self, request, context):
        if self.slowed:
            return store_pb2.VoteResponse(vote=False)
        return store_pb2.VoteResponse(vote=True)

    def doCommit(self, request, context):
        self.storage[request.key] = request.value
        if self.storage[request.key]:
            return store_pb2.CommitResponse(committed=True)
        else:
            return store_pb2.CommitResponse(committed=False)

    def doAbort(self, request, context):
        if self.storage.get(request.key):
            del self.storage[request.key]
        return store_pb2.Empty()

    def askVote(self, request, context):
        if request.key in self.storage:
            return store_pb2.VoteResponse(vote=True, value=self.storage[request.key])
        else:
            return store_pb2.VoteResponse(vote=False, value=None)


def serve():
    config_path = os.path.join('decentralized_config.yaml')
    with open(config_path, 'r') as file:
        conf = yaml.safe_load(file)

    # start slave nodes
    nodes = []
    for node in conf['nodes']:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        address = f"{node['ip']}:{node['port']}"
        weight = node['weight']

        addr2 = random.choice(conf['nodes'])
        while node == addr2:
            addr2 = random.choice(conf['nodes'])

        store_pb2_grpc.add_KeyValueStoreServicer_to_server(DecentralizedStorageSystem(addr=address, weight=weight, neighbor=addr2), server)
        server.add_insecure_port(address)
        server.start()
        nodes.append(server)
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        for node in nodes:
            node.stop(0)

if __name__ == "__main__":
    serve()