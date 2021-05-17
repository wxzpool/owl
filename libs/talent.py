#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import multiprocessing
import time
from libs import daemon
from libs.common import ProcessStatus
import signal

MpManagerDict = dict


class TalentCFG(object):
    db_file: str = "/var/run/owl/talent.db"
    
    
class Talent(multiprocessing.Process):
    """
    Talent 是负责与
    """
    _manager: MpManagerDict = None
    _app_cfg: TalentCFG
    _app_status: ProcessStatus
    # prometheus_host = "127.0.0.1"
    
    def __init__(self, cfg: TalentCFG, manager: MpManagerDict = None, debug: bool = False, *args, **kwargs):
        self.cfg = cfg
        self._debug = debug
        if manager is not None:
            self._manager = manager

        print("Start Success")
        daemon.output_to_log(stdout='/tmp/glue_stdout.log', stderr='/tmp/glue_stderr.log')
        super().__init__(*args, **kwargs)
    
    @property
    def debug(self) -> bool:
        return self._debug
    
    @property
    def cfg(self) -> TalentCFG:
        return self._app_cfg
    
    @cfg.setter
    def cfg(self, val: TalentCFG):
        self._app_cfg = val
    
    def _send_message(self):
        # todo 发送报警
        pass
    
    def _d(self, msg):
        if self._debug:
            print('[PID: %d] [%.3f] %s' % (os.getpid(), time.time(), msg))
            sys.stdout.flush()
    
    def _start_sock_logger(self):
        pass
    
    def _app_check(self):
        if self._app_cfg is None:
            raise RuntimeError('cfg not defined')
    
    def terminate(self, *args, **kwargs):
        print('PID:%s 收到退出请求' % os.getpid())
        sys.stdout.flush()
        raise SystemExit(0)
    
    def run(self):
        d = self._d
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d('初始化启动')
        self._app_check()
        

