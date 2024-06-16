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
        if neighbor:
            try:
                neigh_address = f"{neighbor['ip']}:{neighbor['port']}"
                channel = grpc.insecure_channel(neigh_address)
                stub = store_pb2_grpc.KeyValueStoreStub(channel=channel)

                stub.registerNode(store_pb2.RegisterRequest(address=self.address, weight=self.weight))
                self.nodes[neigh_address] = stub, weight      
            except Exception as e:
                print(e)
        
        
    def registerNode(self, request, context):
        try:
            weight = request.weight
            if request.address not in self.nodes:
                channel = grpc.insecure_channel(request.address)
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                self.nodes[request.address] = stub, weight
            else:
                stub, weight = self.nodes.get(request.address)

            return store_pb2.Empty()   
        except Exception as e:
            print("pasa aqui le error", e)
            return store_pb2.Empty()   

    def gossip(self, request, context):
        print("yow?")
        # obtain an address which isn't self nor request.address
        l = list(self.nodes.keys())
        i = 0
        address = l[0]
        while i < len(l) and l[i] == request.address:
            address = l[i]
            i += 1
        print("yow?2")
        return store_pb2.GossipResponse(address=address, weight=self.nodes[address][1])

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
            try:
                if len(self.nodes) > 1:
                    address, tuple = random.choice(list(self.nodes.items()))
                else:
                    address, tuple = list(self.nodes.items()).pop()
                
                stub = tuple[0]
                weight = tuple[1]

                
                response = stub.gossip(store_pb2.GossipRequest(address=self.address, weight=self.weight))
                if response.address not in self.nodes:
                    channel = grpc.insecure_channel(response.address)
                    stub = store_pb2_grpc.KeyValueStoreStub(channel)
                    stub.registerNode(store_pb2.RegisterRequest(address=self.address, weight=self.weight))
                    self.nodes[response.address] = stub, weight

                key = request.key
                value = request.value
                quorum = self.weight

                for stub, weight in self.nodes.values():
                    try:
                        vote_request = store_pb2.VoteRequest(key=key)
                        vote_response = stub.canCommit(vote_request)
                        if vote_response.vote:
                            quorum += weight
                    except Exception:
                        pass    

                if quorum >= self.weight_for_writes:
                    commit_quorum = self.weight
                    for stub, weight in self.nodes.values():
                        try:
                            commit_request = store_pb2.CommitRequest(key=key, value=value)
                            commit_response = stub.doCommit(commit_request)
                            if commit_response.committed:
                                commit_quorum += weight
                        except Exception:
                            pass

                    if commit_quorum >= self.weight_for_writes:
                        self.storage[key] = value
                        self.write_to_consistency_file(self.consistency_file, key, value)
                        return store_pb2.PutResponse(success=True)
                    else:
                        self.write_to_consistency_file(self.consistency_file, "no", "ce guarda")
                        for stub, weight in self.nodes.values():
                            req = store_pb2.AbortRequest(key=key)
                            stub.doAbort(req)
                        return store_pb2.PutResponse(success=False)
                else:
                    self.write_to_consistency_file(self.consistency_file, "len(nodes)", len(self.nodes))
                    return store_pb2.PutResponse(success=False)
            except Exception as e:
                print("yow", e)
                return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        if self.slowed:
            return store_pb2.GetResponse(value=None, found=False)
        else:
            key = request.key
            quorum_weights = {}

            quorum_weights[self.storage[key]] = self.weight            
            for address, pair in self.nodes.items():
                vote_request = store_pb2.VoteRequest(key=key)
                vote_response = pair[0].askVote(vote_request)
                if vote_response.vote:
                    quorum_weights[vote_response.value] += pair[1]
                else:
                    quorum_weights[vote_response.value] = pair[1]
            
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
            self.write_to_consistency_file(self.consistency_file, key=request.key, value=request.value)
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

    # must start one node with no neighbors first
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node0 = conf['nodes'][0]
    address0 = f"{node0['ip']}:{node0['port']}"
    weight0 = node0['weight']

    store_pb2_grpc.add_KeyValueStoreServicer_to_server(DecentralizedStorageSystem(addr=address0, weight=weight0, neighbor=None), server)
    server.add_insecure_port(address0)
    server.start()
    nodes.append(server)

    # start a second one with connection to the first to ensure the first doesn't stay isolated
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node1 = conf['nodes'][1]
    address1 = f"{node1['ip']}:{node1['port']}"
    weight1 = node1['weight']

    store_pb2_grpc.add_KeyValueStoreServicer_to_server(DecentralizedStorageSystem(addr=address1, weight=weight1, neighbor=node0), server)
    server.add_insecure_port(address1)
    server.start()
    nodes.append(server)

    # finally in a realistic scenario we would have a loop for all other remaining nodes but we only have one left
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node2 = conf['nodes'][2]
    address2 = f"{node2['ip']}:{node2['port']}"
    weight2 = node2['weight']

    neigh = random.choice(conf['nodes'])
    while node2 == neigh:
        neigh = random.choice(conf['nodes'])

    store_pb2_grpc.add_KeyValueStoreServicer_to_server(DecentralizedStorageSystem(addr=address2, weight=weight2, neighbor=neigh), server)
    server.add_insecure_port(address2)
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