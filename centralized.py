import os
import yaml 
import grpc
import time
from concurrent import futures
from proto import store_pb2, store_pb2_grpc

class StorageSystem(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, master, addr=None):
        self.storage = []
        self.delay = 0

        if not addr:
            self.address = master
            self.slave_channels = []
            self.slave_stubs = []
        else:
            self.address = addr
            self.channel = grpc.insecure_channel(master)
            self.stub = store_pb2_grpc.KeyValueStoreStub(self.channel)
            request = store_pb2.RegisterRequest(address=self.address)
            self.stub.registerNode(request)

    def registerNode(self, request, context):
        channel = grpc.insecure_channel(request=address)
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        self.slave_channels.append(channel)
        self.slave_stubs.append(stub)
        return store_pb2.Empty()

    def put(self, request, context):
        commit = True
        for stub in self.slave_stubs:
            request = store_pb2.VoteRequest(key=request.key)
            response = stub.canCommit(request)
            commit = commit and response.vote
        
        if commit:
            comitted = True
            for stub in self.slave_stubs:
                request = store_pb2.CommitRequest(key=request.key, value=request.value)
                response = stub.doCommit(request)
                committed = committed and response.comitted

            if comitted:
                self.storage[request.key] = request.value
                return store_pb2.PutResponse(success=True)
            else:
                for stub in self.slave_stubs:
                    request = store_pb2.AbortRequest(key=request.key, value=request.value)
                    stub.doAbort(request)
                return store_pb2.PutResponse(success=False)
        else:
            return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        val = self.storage[request.key]

        time.sleep(self.delay)

        if val:
            return store_pb2.GetResponse(value=val, found=True)
        else:
            return store_pb2.GetResponse(value=None, found=False)
        
    def slowDown(self, request, context):
        self.delay += request.seconds
        time.sleep(self.delay)

        return store_pb2.SlowDownResponse(success=True)

    def restore(self, request, context):
        self.delay = 0
        return store_pb2.RestoreResponse(success=True)



def serve():
    config_path = os.path.join('centralized_config.yaml')
    with open(config_path, 'r') as file:
        conf = yaml.safe_load(file)

    # start master node
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    master_address = f"{conf['master']['ip']}:{conf['master']['port']}"
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageSystem(master=master_address), master)
    master.add_insecure_port(master_address)
    master.start()
    master.wait_for_termination()

    # start slave nodes
    for slave in conf['slaves']:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        address = f"{slave['ip']}:{slave['port']}"
        store_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageSystem(master=master_address, addr=address), server=server)
        server.add_insecure_port(address)
        server.start()
        server.wait_for_termination()
    
    

if __name__ == "__main__":
    serve()