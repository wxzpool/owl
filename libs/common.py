#!/usr/bin/env python3
# encoding: utf-8


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

