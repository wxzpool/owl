#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import multiprocessing
import time
from libs import daemon
from libs.common import ProcessStatus
from libs.log_receiver import LogReceiverCFG, LogReceiver
import signal
import subprocess
import shlex
import datetime

MpManagerDict = dict


class ShellExeTimeout(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def exec_shell(cmd, cwd=None, timeout=None, shell=False):
    """
        封装一个执行shell的方法
        封装了subprocess的Popen方法，支持超时判断，支持读取stdout和stderr
        参数：
            cwd: 运行路径，如果被设定，子进程会切换到cwd
            timeout: 超时时间， 秒， 支持小数，精度0.1秒
            shell: 是否通过shell运行
        返回： [return_code(int),'stdout(file handle)','stderr(file handle)']
        Raises: ShellExeTimeout: 执行超时
        在外部捕捉此错误
        注意：如果命令带有管道，必须用shell=True

    :param cmd:  string, 执行的命令
    :param cwd:  string, 运行路径，如果被设定，子进程会切换到cwd
    :param timeout:  float, 超时时间， 秒， 支持小数，精度0.1秒
    :param shell:  bool, 是否通过shell运行
    :return:  list, [return_code(int),'stdout(file handle)','stderr(file handle)']
    :raise ShellExeTimeout: 运行超时
    """
    try:
        if shell:
            cmd_list = cmd
        else:
            cmd_list = shlex.split(cmd)
        if timeout is not None:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        sub = subprocess.Popen(cmd_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while sub.poll() is None:
            time.sleep(0.1)
            if timeout is not None:
                if end_time < datetime.datetime.now():
                    raise ShellExeTimeout("Shell Run Timeout(%s sec): %s" % (timeout,cmd))
        return [int(sub.returncode), sub.stdout, sub.stderr]
    except OSError as e:
        return [1, [], [e]]


class SupervisorCFG(object):
    __name: str
    __sock_path: str = "/tmp"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def sock_path(self) -> str:
        return self.__sock_path
    
    def __init__(self, name: str, sock_path: str = None):
        self.__name = name
        if sock_path is not None:
            self.__sock_path = sock_path
            
    
class Supervisor(multiprocessing.Process):
    _app_cfg: SupervisorCFG
    _manager: MpManagerDict = None
    _app_status: ProcessStatus
    prometheus_host = "127.0.0.1"
    
    def __init__(self, cfg: SupervisorCFG, manager: dict = None, debug: bool = False, *args, **kwargs):
        self._app_cfg = cfg
        self._debug = debug
        self._sock_file = "%s/%s.sock" % (self.cfg.sock_path, self.cfg.name)
        if manager is not None:
            self._manager = manager
        log_server_cfg = LogReceiverCFG(
        
        )
        log_server = LogReceiver()
        print("Start Success")
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
            print('[PID: %d] [%.3f] %s' % (os.getpid(), time.time(), msg))
            sys.stdout.flush()
    
    def _start_sock_logger(self):
        logger_cfg = LogReceiverCFG(
            name=self._sock_file,
            sock_path=self.cfg.sock_path
        )
        logger = LogReceiver(logger_cfg)
        self._logger = logger
        logger.daemon = True
        logger.start()
    
    def _check_runtime(self):
        if self.cfg is None:
            raise RuntimeError('cfg not defined')
    
    def terminate(self, *args, **kwargs):
        print('%s收到退出请求' % os.getpid())
        sys.stdout.flush()
        # 关闭log
        logger = self._logger
        if logger.is_alive():
            os.kill(logger.pid, signal.SIGTERM)
        raise SystemExit(0)
    
    def run(self):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d = self._d
        d('初始化启动')
        self._check_runtime()
        # 阻塞，获取任务
        
        
        
        

