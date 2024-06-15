# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from proto import store_pb2 as proto_dot_store__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in proto/store_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class KeyValueStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.put = channel.unary_unary(
                '/distributedstore.KeyValueStore/put',
                request_serializer=proto_dot_store__pb2.PutRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.PutResponse.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/distributedstore.KeyValueStore/get',
                request_serializer=proto_dot_store__pb2.GetRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.GetResponse.FromString,
                _registered_method=True)
        self.slowDown = channel.unary_unary(
                '/distributedstore.KeyValueStore/slowDown',
                request_serializer=proto_dot_store__pb2.SlowDownRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.SlowDownResponse.FromString,
                _registered_method=True)
        self.restore = channel.unary_unary(
                '/distributedstore.KeyValueStore/restore',
                request_serializer=proto_dot_store__pb2.RestoreRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.RestoreResponse.FromString,
                _registered_method=True)
        self.registerNode = channel.unary_unary(
                '/distributedstore.KeyValueStore/registerNode',
                request_serializer=proto_dot_store__pb2.RegisterRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.Empty.FromString,
                _registered_method=True)
        self.canCommit = channel.unary_unary(
                '/distributedstore.KeyValueStore/canCommit',
                request_serializer=proto_dot_store__pb2.VoteRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.VoteResponse.FromString,
                _registered_method=True)
        self.doCommit = channel.unary_unary(
                '/distributedstore.KeyValueStore/doCommit',
                request_serializer=proto_dot_store__pb2.CommitRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.CommitResponse.FromString,
                _registered_method=True)
        self.doAbort = channel.unary_unary(
                '/distributedstore.KeyValueStore/doAbort',
                request_serializer=proto_dot_store__pb2.AbortRequest.SerializeToString,
                response_deserializer=proto_dot_store__pb2.Empty.FromString,
                _registered_method=True)
        self.ping = channel.unary_unary(
                '/distributedstore.KeyValueStore/ping',
                request_serializer=proto_dot_store__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_store__pb2.PingResponse.FromString,
                _registered_method=True)


class KeyValueStoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def slowDown(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def restore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def canCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doAbort(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyValueStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'put': grpc.unary_unary_rpc_method_handler(
                    servicer.put,
                    request_deserializer=proto_dot_store__pb2.PutRequest.FromString,
                    response_serializer=proto_dot_store__pb2.PutResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=proto_dot_store__pb2.GetRequest.FromString,
                    response_serializer=proto_dot_store__pb2.GetResponse.SerializeToString,
            ),
            'slowDown': grpc.unary_unary_rpc_method_handler(
                    servicer.slowDown,
                    request_deserializer=proto_dot_store__pb2.SlowDownRequest.FromString,
                    response_serializer=proto_dot_store__pb2.SlowDownResponse.SerializeToString,
            ),
            'restore': grpc.unary_unary_rpc_method_handler(
                    servicer.restore,
                    request_deserializer=proto_dot_store__pb2.RestoreRequest.FromString,
                    response_serializer=proto_dot_store__pb2.RestoreResponse.SerializeToString,
            ),
            'registerNode': grpc.unary_unary_rpc_method_handler(
                    servicer.registerNode,
                    request_deserializer=proto_dot_store__pb2.RegisterRequest.FromString,
                    response_serializer=proto_dot_store__pb2.Empty.SerializeToString,
            ),
            'canCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.canCommit,
                    request_deserializer=proto_dot_store__pb2.VoteRequest.FromString,
                    response_serializer=proto_dot_store__pb2.VoteResponse.SerializeToString,
            ),
            'doCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.doCommit,
                    request_deserializer=proto_dot_store__pb2.CommitRequest.FromString,
                    response_serializer=proto_dot_store__pb2.CommitResponse.SerializeToString,
            ),
            'doAbort': grpc.unary_unary_rpc_method_handler(
                    servicer.doAbort,
                    request_deserializer=proto_dot_store__pb2.AbortRequest.FromString,
                    response_serializer=proto_dot_store__pb2.Empty.SerializeToString,
            ),
            'ping': grpc.unary_unary_rpc_method_handler(
                    servicer.ping,
                    request_deserializer=proto_dot_store__pb2.Empty.FromString,
                    response_serializer=proto_dot_store__pb2.PingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'distributedstore.KeyValueStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('distributedstore.KeyValueStore', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class KeyValueStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/put',
            proto_dot_store__pb2.PutRequest.SerializeToString,
            proto_dot_store__pb2.PutResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/get',
            proto_dot_store__pb2.GetRequest.SerializeToString,
            proto_dot_store__pb2.GetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def slowDown(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/slowDown',
            proto_dot_store__pb2.SlowDownRequest.SerializeToString,
            proto_dot_store__pb2.SlowDownResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def restore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/restore',
            proto_dot_store__pb2.RestoreRequest.SerializeToString,
            proto_dot_store__pb2.RestoreResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def registerNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/registerNode',
            proto_dot_store__pb2.RegisterRequest.SerializeToString,
            proto_dot_store__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def canCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/canCommit',
            proto_dot_store__pb2.VoteRequest.SerializeToString,
            proto_dot_store__pb2.VoteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def doCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/doCommit',
            proto_dot_store__pb2.CommitRequest.SerializeToString,
            proto_dot_store__pb2.CommitResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def doAbort(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/doAbort',
            proto_dot_store__pb2.AbortRequest.SerializeToString,
            proto_dot_store__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/ping',
            proto_dot_store__pb2.Empty.SerializeToString,
            proto_dot_store__pb2.PingResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
