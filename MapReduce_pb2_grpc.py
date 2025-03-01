# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import MapReduce_pb2 as MapReduce__pb2


class MapperServiceStub(object):
    """Service defination for the Mapper
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.perform_map = channel.unary_unary(
                '/kmeans.MapperService/perform_map',
                request_serializer=MapReduce__pb2.MapperParameters.SerializeToString,
                response_deserializer=MapReduce__pb2.MapperResponse.FromString,
                )
        self.send_data_to_reducer = channel.unary_unary(
                '/kmeans.MapperService/send_data_to_reducer',
                request_serializer=MapReduce__pb2.ReducerParameters.SerializeToString,
                response_deserializer=MapReduce__pb2.ReducerResponse.FromString,
                )


class MapperServiceServicer(object):
    """Service defination for the Mapper
    """

    def perform_map(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def send_data_to_reducer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MapperServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'perform_map': grpc.unary_unary_rpc_method_handler(
                    servicer.perform_map,
                    request_deserializer=MapReduce__pb2.MapperParameters.FromString,
                    response_serializer=MapReduce__pb2.MapperResponse.SerializeToString,
            ),
            'send_data_to_reducer': grpc.unary_unary_rpc_method_handler(
                    servicer.send_data_to_reducer,
                    request_deserializer=MapReduce__pb2.ReducerParameters.FromString,
                    response_serializer=MapReduce__pb2.ReducerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'kmeans.MapperService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MapperService(object):
    """Service defination for the Mapper
    """

    @staticmethod
    def perform_map(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kmeans.MapperService/perform_map',
            MapReduce__pb2.MapperParameters.SerializeToString,
            MapReduce__pb2.MapperResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def send_data_to_reducer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kmeans.MapperService/send_data_to_reducer',
            MapReduce__pb2.ReducerParameters.SerializeToString,
            MapReduce__pb2.ReducerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ReducerServiceStub(object):
    """Service defination for the Reducer
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.invoke_reducer = channel.unary_unary(
                '/kmeans.ReducerService/invoke_reducer',
                request_serializer=MapReduce__pb2.InvokeParameters.SerializeToString,
                response_deserializer=MapReduce__pb2.InvokeResponse.FromString,
                )


class ReducerServiceServicer(object):
    """Service defination for the Reducer
    """

    def invoke_reducer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReducerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'invoke_reducer': grpc.unary_unary_rpc_method_handler(
                    servicer.invoke_reducer,
                    request_deserializer=MapReduce__pb2.InvokeParameters.FromString,
                    response_serializer=MapReduce__pb2.InvokeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'kmeans.ReducerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReducerService(object):
    """Service defination for the Reducer
    """

    @staticmethod
    def invoke_reducer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kmeans.ReducerService/invoke_reducer',
            MapReduce__pb2.InvokeParameters.SerializeToString,
            MapReduce__pb2.InvokeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
