# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mychatbot_pb2 as mychatbot__pb2


class simplechatbotStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.predict = channel.unary_unary(
                '/simplechatbot.simplechatbot/predict',
                request_serializer=mychatbot__pb2.predict_req.SerializeToString,
                response_deserializer=mychatbot__pb2.predict_resp.FromString,
                )


class simplechatbotServicer(object):
    """Missing associated documentation comment in .proto file."""

    def predict(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_simplechatbotServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'predict': grpc.unary_unary_rpc_method_handler(
                    servicer.predict,
                    request_deserializer=mychatbot__pb2.predict_req.FromString,
                    response_serializer=mychatbot__pb2.predict_resp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'simplechatbot.simplechatbot', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class simplechatbot(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def predict(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/simplechatbot.simplechatbot/predict',
            mychatbot__pb2.predict_req.SerializeToString,
            mychatbot__pb2.predict_resp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
