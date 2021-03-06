# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import talent_pb2 as talent__pb2


class PlotManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.plot_task_create = channel.unary_unary(
                '/talent.PlotManager/plot_task_create',
                request_serializer=talent__pb2.PlotTaskCreateRequest.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatusResponse.FromString,
                )
        self.plot_task_status = channel.unary_unary(
                '/talent.PlotManager/plot_task_status',
                request_serializer=talent__pb2.PlotTaskIdRequest.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatus.FromString,
                )
        self.plot_task_status_all = channel.unary_unary(
                '/talent.PlotManager/plot_task_status_all',
                request_serializer=talent__pb2.Empty.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatusAllResponse.FromString,
                )
        self.plot_task_stop = channel.unary_unary(
                '/talent.PlotManager/plot_task_stop',
                request_serializer=talent__pb2.PlotTaskStopRequest.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatusResponse.FromString,
                )
        self.plot_task_update = channel.unary_unary(
                '/talent.PlotManager/plot_task_update',
                request_serializer=talent__pb2.PlotTaskStatus.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskUpdateResponse.FromString,
                )
        self.get_plot_tasks = channel.unary_unary(
                '/talent.PlotManager/get_plot_tasks',
                request_serializer=talent__pb2.PlotStatus.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatusAllResponse.FromString,
                )
        self.get_plot_by_cache = channel.unary_unary(
                '/talent.PlotManager/get_plot_by_cache',
                request_serializer=talent__pb2.GetPlotByCacheRequest.SerializeToString,
                response_deserializer=talent__pb2.PlotTaskStatusAllResponse.FromString,
                )


class PlotManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def plot_task_create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def plot_task_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def plot_task_status_all(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def plot_task_stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def plot_task_update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_plot_tasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_plot_by_cache(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PlotManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'plot_task_create': grpc.unary_unary_rpc_method_handler(
                    servicer.plot_task_create,
                    request_deserializer=talent__pb2.PlotTaskCreateRequest.FromString,
                    response_serializer=talent__pb2.PlotTaskStatusResponse.SerializeToString,
            ),
            'plot_task_status': grpc.unary_unary_rpc_method_handler(
                    servicer.plot_task_status,
                    request_deserializer=talent__pb2.PlotTaskIdRequest.FromString,
                    response_serializer=talent__pb2.PlotTaskStatus.SerializeToString,
            ),
            'plot_task_status_all': grpc.unary_unary_rpc_method_handler(
                    servicer.plot_task_status_all,
                    request_deserializer=talent__pb2.Empty.FromString,
                    response_serializer=talent__pb2.PlotTaskStatusAllResponse.SerializeToString,
            ),
            'plot_task_stop': grpc.unary_unary_rpc_method_handler(
                    servicer.plot_task_stop,
                    request_deserializer=talent__pb2.PlotTaskStopRequest.FromString,
                    response_serializer=talent__pb2.PlotTaskStatusResponse.SerializeToString,
            ),
            'plot_task_update': grpc.unary_unary_rpc_method_handler(
                    servicer.plot_task_update,
                    request_deserializer=talent__pb2.PlotTaskStatus.FromString,
                    response_serializer=talent__pb2.PlotTaskUpdateResponse.SerializeToString,
            ),
            'get_plot_tasks': grpc.unary_unary_rpc_method_handler(
                    servicer.get_plot_tasks,
                    request_deserializer=talent__pb2.PlotStatus.FromString,
                    response_serializer=talent__pb2.PlotTaskStatusAllResponse.SerializeToString,
            ),
            'get_plot_by_cache': grpc.unary_unary_rpc_method_handler(
                    servicer.get_plot_by_cache,
                    request_deserializer=talent__pb2.GetPlotByCacheRequest.FromString,
                    response_serializer=talent__pb2.PlotTaskStatusAllResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'talent.PlotManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PlotManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def plot_task_create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/plot_task_create',
            talent__pb2.PlotTaskCreateRequest.SerializeToString,
            talent__pb2.PlotTaskStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def plot_task_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/plot_task_status',
            talent__pb2.PlotTaskIdRequest.SerializeToString,
            talent__pb2.PlotTaskStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def plot_task_status_all(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/plot_task_status_all',
            talent__pb2.Empty.SerializeToString,
            talent__pb2.PlotTaskStatusAllResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def plot_task_stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/plot_task_stop',
            talent__pb2.PlotTaskStopRequest.SerializeToString,
            talent__pb2.PlotTaskStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def plot_task_update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/plot_task_update',
            talent__pb2.PlotTaskStatus.SerializeToString,
            talent__pb2.PlotTaskUpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_plot_tasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/get_plot_tasks',
            talent__pb2.PlotStatus.SerializeToString,
            talent__pb2.PlotTaskStatusAllResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_plot_by_cache(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/talent.PlotManager/get_plot_by_cache',
            talent__pb2.GetPlotByCacheRequest.SerializeToString,
            talent__pb2.PlotTaskStatusAllResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
