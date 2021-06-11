#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import multiprocessing
# import threading
import time
from libs.sturcts import ProcessStatus, PlotterCFG
import signal
import subprocess
import shlex
import datetime
import socket
import time
import psutil

MpManagerDict = dict


class Plotter(multiprocessing.Process):
    # class Plotter(threading.Thread):
    """
    实际任务
    """
    _manager: MpManagerDict = None
    _app_cfg: PlotterCFG
    _app_status: ProcessStatus
    _plotter = None
    # pid: int
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
        _name = "Plotter-%s" % self.cfg.task_id
        _pid = os.getpid()
        _now = time.time()
        if self._debug:
            print('[%s]-[PID: %d]-[%.3f] %s' % (_name, _pid, _now, msg))
        with open("%s/plotter-%s.log" %(self.cfg.log_store, self.cfg.name), "a") as log:
            log.write('[PID: %d] [%.3f] %s\n' % (_pid, _now, msg))
            log.flush()
    
    def _start_sock_logger(self):
        pass
    
    def _app_check(self):
        if self._app_cfg is None:
            raise RuntimeError('cfg not defined')
    
    def terminate(self, *args, **kwargs):
        exit_code = 0
        d = self._d
        d('PID:%s Plotter 收到退出请求' % self.pid)
        sys.stdout.flush()
        if self._plotter.pid is not None and psutil.pid_exists(self._plotter.pid):
            os.kill(self._plotter.pid, 9)
        d("Plotter stopped")
        if 'exit_code' in kwargs:
            exit_code = kwargs['exit_code']
        raise SystemExit(exit_code)
    
    def run(self):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d = self._d
        # self.pid = os.getpid()
        d("sleep 1 for supervisor write back status")
        time.sleep(1)
        # signal.signal(signal.SIGTERM, self.terminate)
        # signal.signal(signal.SIGINT, self.terminate)
        d("Start Plotter, pid=%s" % self.pid)
        self._app_check()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        s.connect(self.sock_file)
        file_handle = s.makefile('wb')
        cmd = "{python} {bin} plots create -k {ksize} -r {thread} -b {mem} -f {fpk} -p {ppk} -t {cache1} -2 {cache2} -d {dest}".format(
            python=self.cfg.python,
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
        # d(cmd)
        self._plotter = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, bufsize=4096, stdout=file_handle, stderr=subprocess.PIPE)
        # d(dir(self._plotter))
        self._plotter.wait()
        
        d("run done, rt: %s" % self._plotter.returncode)
        d("stderr: %s" % self._plotter.stderr.read())
        # raise SystemExit(self._plotter.returncode)
        return self.terminate(exit_code=self._plotter.returncode)

