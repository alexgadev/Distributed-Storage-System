import os
import yaml 
import grpc
import time
from concurrent import futures
from proto import store_pb2, store_pb2_grpc

class CentralizedStorageSystem(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, master, addr=None):
        self.storage = {}
        self.delay = 0
        self.slowed = False
        self.consistency_file = f"centralized_recovery_file.txt"

        self.recover_from_failure(self.consistency_file)

        if not addr: # master node
            self.address = master
            self.slave_channels = []
            self.slave_stubs = []
        else: # slave node
            self.address = addr
            self.channel = grpc.insecure_channel(master)
            self.stub = store_pb2_grpc.KeyValueStoreStub(self.channel)
            request = store_pb2.RegisterRequest(address=self.address)
            self.stub.registerNode(request)

    def registerNode(self, request, context):
        channel = grpc.insecure_channel(request.address)
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        self.slave_channels.append(channel)
        self.slave_stubs.append(stub)
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
            available = True
            for stub in self.slave_stubs:
                vote_request = store_pb2.VoteRequest(key=request.key)
                vote_response = stub.canCommit(vote_request)
                available = available & vote_response.vote

            if available:
                commit = True
                for stub in self.slave_stubs:
                    commit_request = store_pb2.CommitRequest(key=request.key, value=request.value)
                    commit_response = stub.doCommit(commit_request)
                    commit = commit & commit_response.committed

                if commit:
                    self.storage[request.key] = request.value
                    self.write_to_consistency_file(self.consistency_file, request.key, request.value)
                    return store_pb2.PutResponse(success=True)
                else:
                    for stub in self.slave_stubs:
                        req = store_pb2.AbortRequest(key=request.key)
                        stub.doAbort(req)
                    return store_pb2.PutResponse(success=False)
            else:
                return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        if self.slowed:
            return store_pb2.GetResponse(value=None, found=False)
        else:
            val = self.storage.get(request.key)
            if val:
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
        return store_pb2.CommitResponse(committed=True)
    
    def doAbort(self, request, context):
        if self.storage.get(request.key):
            del self.storage[request.key]
        return store_pb2.Empty()


def serve():
    config_path = os.path.join('centralized_config.yaml')
    with open(config_path, 'r') as file:
        conf = yaml.safe_load(file)

    # start master node
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    master_address = f"{conf['master']['ip']}:{conf['master']['port']}"
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(CentralizedStorageSystem(master=master_address), master)
    master.add_insecure_port(master_address)
    master.start()

    # start slave nodes
    slaves = []
    for slave in conf['slaves']:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        address = f"{slave['ip']}:{slave['port']}"
        store_pb2_grpc.add_KeyValueStoreServicer_to_server(CentralizedStorageSystem(master=master_address, addr=address), server)
        server.add_insecure_port(address)
        server.start()
        slaves.append(server)
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        for slave in slaves:
            slave.stop(0)

if __name__ == "__main__":
    serve()