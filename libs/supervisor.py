#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import multiprocessing
import time
from libs import daemon
from libs.common import ProcessStatus
from libs.log_receiver import LogReceiverCFG, LogReceiver
from libs.plotter import PlotterCFG, Plotter
import signal
from copy import deepcopy
import subprocess
import shlex
import datetime
import socket

MpManagerDict = dict


class ProcessList(object):
    plotter: Plotter
    logger: LogReceiver


class SupervisorCFG(object):
    sock_path: str = "/tmp"
    
    
class Supervisor(multiprocessing.Process):
    _app_cfg: SupervisorCFG
    _manager: MpManagerDict = None
    _app_status: ProcessStatus
    _process_list: [ProcessList] = list()
    
    def __init__(self, cfg: SupervisorCFG, manager: dict = None, debug: bool = False, *args, **kwargs):
        self._app_cfg = cfg
        self._debug = debug
        # self._sock_file = "%s/%s.sock" % (self.cfg.sock_path, self.cfg.name)
        if manager is not None:
            self._manager = manager
        # print("Start Success")
        # daemon.output_to_log(stdout='/tmp/glue_stdout.log', stderr='/tmp/glue_stderr.log')
        
        super().__init__(*args, **kwargs)
    
    @property
    def debug(self) -> bool:
        return self._debug
    
    @property
    def cfg(self) -> SupervisorCFG:
        return self._app_cfg
    
    @cfg.setter
    def cfg(self, val: SupervisorCFG):
        self._app_cfg = val
    
    def _send_message(self):
        # todo 发送报警
        pass
    
    def _d(self, msg):
        if self._debug:
            with open("/tmp/supervisor.log", "a") as log:
                log.write('[PID: %d] [%.3f] %s' % (os.getpid(), time.time(), msg))
                log.flush()
    
    def _start_sock_logger(self, name, sock_path) -> LogReceiver:
        logger_cfg = LogReceiverCFG()
        logger_cfg.name = name
        logger_cfg.sock_path = sock_path
        logger = LogReceiver(logger_cfg, debug=self.debug)
        logger.daemon = True
        logger.start()
        return logger

    def _start_plotter(self, cfg: PlotterCFG, sock_file: str):
        plotter = Plotter(cfg, sock_file, debug=self._debug)
        plotter.daemon = True
        plotter.start()
        return plotter
    
    def _check_runtime(self):
        if self.cfg is None:
            raise RuntimeError('cfg not defined')
    
    @staticmethod
    def _get_task() -> list:
        # 返回的是一个PlotProcessCFG元素的数组
        from time import time
        now = int(time())
        p = PlotterCFG()
        p.bin = "/tmp/chia"
        p.name = "tester_%s" % now
        p.fpk = "fpk1"
        p.ppk = "ppk1"
        p.thread = 4
        p.ksize = 33
        p.cache1 = "/cache/level1-1"
        p.cache2 = p.cache1
        p.dest = "/data/1"
        p.mem = 8000
        p2 = deepcopy(p)
        p3 = deepcopy(p)
        p2.name = "tester_%s" % int(time())
        p2.dest = "/data/2"
        p3.name = "tester_%s" % int(time())
        p3.dest = "/data/3"
        return [p, p2, p3]
    
    def terminate(self, *args, **kwargs):
        d = self._d
        print('PID:%s Supervisor 收到退出请求' % os.getpid())
        sys.stdout.flush()
        # todo Supervisor管理了多个的p图进程，需要遍历并关闭他们
        # 关闭log
        # logger = self._logger
        # if logger.is_alive():
        #    os.kill(logger.pid, signal.SIGTERM)
        for pl in self._process_list:
            print("关闭子进程plotter: %s, logger: %s" % (pl.plotter.pid, pl.logger.pid))
            os.kill(pl.plotter.pid, signal.SIGKILL)
            os.kill(pl.logger.pid, signal.SIGTERM)
        raise SystemExit(0)
    
    def run(self):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d = self._d
        _pid = os.getpid()
        print("Start Supervisor, pid=%s" % _pid)
        self._check_runtime()
        # 检查现有任务状态
        for pl in self._process_list:
            d(pl.plotter.pid)
        # 定时获取任务， grpc调用talent
        for t in self._get_task():
            # todo 机器应该有最大上限(按照ssd划分)
            process = ProcessList()
            # print("start logger")
            process.logger = self._start_sock_logger(t.name, self.cfg.sock_path)
            d(process.logger)
            # time.sleep(3)
            # test sock server up
            while True:
                if os.path.exists(process.logger.sock_file):
                    break
                time.sleep(1)
            # print("start plotter")
            process.plotter = self._start_plotter(t, process.logger.sock_file)
            d(process.plotter)
            self._process_list.append(process)
        
        while True:
            # d(self._process_list[0])
            time.sleep(1)
            

        
        
        
        
        

