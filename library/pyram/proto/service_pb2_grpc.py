# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

# This line isn't from code gen, please don't remove
from . import service_pb2 as service__pb2


class RAMServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendEvent = channel.unary_unary(
                '/tekone.library.ram.config.proto.RAMService/SendEvent',
                request_serializer=service__pb2.SendEventRequest.SerializeToString,
                response_deserializer=service__pb2.SendEventResponse.FromString,
                )
        self.ReviveEvent = channel.unary_unary(
                '/tekone.library.ram.config.proto.RAMService/ReviveEvent',
                request_serializer=service__pb2.ReviveEventRequest.SerializeToString,
                response_deserializer=service__pb2.ReviveEventResponse.FromString,
                )
        self.ScheduleSendEvent = channel.unary_unary(
                '/tekone.library.ram.config.proto.RAMService/ScheduleSendEvent',
                request_serializer=service__pb2.ScheduleSendEventRequest.SerializeToString,
                response_deserializer=service__pb2.ScheduleSendEventResponse.FromString,
                )
        self.GetEventStatus = channel.unary_unary(
                '/tekone.library.ram.config.proto.RAMService/GetEventStatus',
                request_serializer=service__pb2.GetEventStatusRequest.SerializeToString,
                response_deserializer=service__pb2.GetEventStatusResponse.FromString,
                )
        self.GetEventStatusById = channel.unary_unary(
                '/tekone.library.ram.config.proto.RAMService/GetEventStatusById',
                request_serializer=service__pb2.GetEventStatusByIdRequest.SerializeToString,
                response_deserializer=service__pb2.GetEventStatusByIdResponse.FromString,
                )


class RAMServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendEvent(self, request, context):
        """Send a new event for processing
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReviveEvent(self, request, context):
        """Ask sender to revive all dead unsent events
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ScheduleSendEvent(self, request, context):
        """trigger a publish of an event
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEventStatus(self, request, context):
        """get the stauts of an event
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEventStatusById(self, request, context):
        """get the stauts of an event
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RAMServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.SendEvent,
                    request_deserializer=service__pb2.SendEventRequest.FromString,
                    response_serializer=service__pb2.SendEventResponse.SerializeToString,
            ),
            'ReviveEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.ReviveEvent,
                    request_deserializer=service__pb2.ReviveEventRequest.FromString,
                    response_serializer=service__pb2.ReviveEventResponse.SerializeToString,
            ),
            'ScheduleSendEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.ScheduleSendEvent,
                    request_deserializer=service__pb2.ScheduleSendEventRequest.FromString,
                    response_serializer=service__pb2.ScheduleSendEventResponse.SerializeToString,
            ),
            'GetEventStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEventStatus,
                    request_deserializer=service__pb2.GetEventStatusRequest.FromString,
                    response_serializer=service__pb2.GetEventStatusResponse.SerializeToString,
            ),
            'GetEventStatusById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEventStatusById,
                    request_deserializer=service__pb2.GetEventStatusByIdRequest.FromString,
                    response_serializer=service__pb2.GetEventStatusByIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tekone.library.ram.config.proto.RAMService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RAMService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tekone.library.ram.config.proto.RAMService/SendEvent',
            service__pb2.SendEventRequest.SerializeToString,
            service__pb2.SendEventResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReviveEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tekone.library.ram.config.proto.RAMService/ReviveEvent',
            service__pb2.ReviveEventRequest.SerializeToString,
            service__pb2.ReviveEventResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ScheduleSendEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tekone.library.ram.config.proto.RAMService/ScheduleSendEvent',
            service__pb2.ScheduleSendEventRequest.SerializeToString,
            service__pb2.ScheduleSendEventResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEventStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tekone.library.ram.config.proto.RAMService/GetEventStatus',
            service__pb2.GetEventStatusRequest.SerializeToString,
            service__pb2.GetEventStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEventStatusById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tekone.library.ram.config.proto.RAMService/GetEventStatusById',
            service__pb2.GetEventStatusByIdRequest.SerializeToString,
            service__pb2.GetEventStatusByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
