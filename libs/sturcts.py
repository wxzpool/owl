#!/usr/bin/env python3
# encoding: utf-8

# from libs.grpc import talent_pb2 as pb2
# from libs.grpc import talent as pb2_ref
#
# PlotPhaseStatus: pb2_ref.PlotPhaseStatus = pb2.PlotPhaseStatus
# PlotP2BaseStatus: pb2_ref.PlotP2BaseStatus = pb2.PlotP2BaseStatus
# PlotP1Status: pb2_ref.PlotP1Status = pb2.PlotP1Status
# PlotP2Status: pb2_ref.PlotP2Status = pb2.PlotP2Status
# PlotP3Status: pb2_ref.PlotP3Status = pb2.PlotP3Status
# PlotP4Status: pb2_ref.PlotPhaseStatus = pb2.PlotPhaseStatus
# PlotDetails: pb2_ref.PlotDetails = pb2.PlotDetails


class ProcessRuntimeStatus(object):
    class StatusError(Exception):
        pass
    __status: str
    __status_list = ["starting", "stopped", "running"]
    
    def __init__(self, s: str):
        if s not in self.__status_list:
            raise ProcessRuntimeStatus.StatusError("%s not in %s" % (s, self.__status_list))
    
    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, s: str):
        if s in self.__status_list:
            self.__status = s
    
    def __repr__(self):
        return self.__status
    
    def __str__(self):
        return self.__status


class ProcessStatus(object):
    id: str = None
    status: ProcessRuntimeStatus
    heartbeat: int


class PlotterCFG(object):
    task_id: str
    log_store: str
    bin: str = "/tmp/chia"
    name: str
    fpk: str
    ppk: str
    thread: int
    mem: int
    cache1: str
    cache2: str
    dest: str
    ksize: int


class CacheCFG(object):
    dest: str
    capacity: int


class PlotProcessCFG(object):
    cap_limit: int = 90
    log_store: str
    bin: str = "/tmp/chia"
    waiting: int = 1200
    cache1: [CacheCFG]
    cache2: [CacheCFG]
    dests: [str]
    
    def get_cache1_info(self, t):
        # print(dir(self))
        # print(t)
        for c in self.cache1:
            if t == c.dest:
                return c.capacity
        return 0


class SupervisorCFG(object):
    sock_path: str = "/tmp"
    grpc_host: str = "127.0.0.1:50051"
    sleep_time: int = 30
    log_file: str
    pid_file: str
    plot_process_config: PlotProcessCFG


