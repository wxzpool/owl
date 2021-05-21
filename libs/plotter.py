#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import multiprocessing
import time
from libs import daemon
from libs.common import ProcessStatus
import signal
import subprocess
import shlex
import datetime
import socket

MpManagerDict = dict


class PlotterCFG(object):
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
    

class Plotter(multiprocessing.Process):
    """
    Talent 是负责与
    """
    _manager: MpManagerDict = None
    _app_cfg: PlotterCFG
    _app_status: ProcessStatus
    _plotter = None
    # prometheus_host = "127.0.0.1"
    
    def __init__(self, cfg: PlotterCFG, sock_file: str, manager: MpManagerDict = None, debug: bool = False, *args, **kwargs):
        self.cfg = cfg
        self.sock_file = sock_file
        self._debug = debug
        if manager is not None:
            self._manager = manager
        # print("Start Success")
        super().__init__(*args, **kwargs)
    
    @property
    def debug(self) -> bool:
        return self._debug
    
    @property
    def cfg(self) -> PlotterCFG:
        return self._app_cfg
    
    @cfg.setter
    def cfg(self, val: PlotterCFG):
        self._app_cfg = val
    
    def _send_message(self):
        # todo 发送报警
        pass
    
    def _d(self, msg):
        if self._debug:
            with open("/tmp/plotter.log", "a") as log:
                log.write('[PID: %d] [%.3f] %s' % (os.getpid(), time.time(), msg))
                log.flush()
    
    def _start_sock_logger(self):
        pass
    
    def _app_check(self):
        if self._app_cfg is None:
            raise RuntimeError('cfg not defined')
    
    def terminate(self, *args, **kwargs):
        print('PID:%s Plotter 收到退出请求' % os.getpid())
        sys.stdout.flush()
        os.kill(self._plotter.pid, 9)
        raise SystemExit(0)
    
    def run(self):
        d = self._d
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        _pid = os.getpid()
        print("Start Plotter, pid=%s" % _pid)
        self._app_check()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        s.connect(self.sock_file)
        file_handle = s.makefile('wb')
        cmd = "{bin} plots create -k {ksize} -r {thread} -b {mem} -f {fpk} -p {ppk} -t {cache1} -2 {cache2} -d {dest}".format(
            bin=self.cfg.bin,
            ksize=self.cfg.ksize,
            thread=self.cfg.thread,
            mem=self.cfg.mem,
            fpk=self.cfg.fpk,
            ppk=self.cfg.ppk,
            cache1=self.cfg.cache1,
            cache2=self.cfg.cache2,
            dest=self.cfg.dest
        )
        d(cmd)
        self._plotter = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, bufsize=4096, stdout=file_handle, stderr=file_handle)
        d(dir(self._plotter))
        

