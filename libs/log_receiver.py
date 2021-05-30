#!/usr/bin/env python3
# encoding: utf-8
# 每个p图进程都会对应一个日志收集人，收集到的日志会统一通讯给talent并由talent上传给octopus
import multiprocessing
from libs.common import ProcessStatus
import os
import sys
import time
import signal
from struct import unpack, calcsize
import socket
from . import log_filter

MpManagerDict = dict


class LogReceiverCFG(object):
    name: str
    sock_path: str


class LogReceiver(multiprocessing.Process):
    _app_cfg: LogReceiverCFG
    _manager: MpManagerDict = None
    _app_status: ProcessStatus
    _log_sock = None

    def __init__(self, cfg: LogReceiverCFG, manager: MpManagerDict = None, debug: bool = False, *args, **kwargs):
        self.cfg = cfg
        self._debug = debug
        self.sock_file = "%s/%s.sock" % (self.cfg.sock_path, self.cfg.name)
        if manager is not None:
            self._manager = manager
        # print("LogReceiver Start Success")
        super().__init__(*args, **kwargs)

    def _d(self, msg):
        _name = "LogReceiver-%s" % self.name
        _pid = os.getpid()
        _now = time.time()
        print('[%s]-[PID: %d]-[%.3f] %s' % (_name, _pid, _now, msg))
        if self._debug:
            with open("/tmp/log_receiver.log", "a") as log:
                log.write('[PID: %d] [%.3f] %s' % ( _pid, _now, msg))
                log.flush()
    
    def terminate(self, *args, **kwargs):
        self._d('PID:%s LogReceiver收到退出请求' % os.getpid())
        sys.stdout.flush()
        if self._log_sock is not None:
            self._log_sock.close()
        try:
            os.remove(self.sock_file)
        except OSError:
            pass
        self._d("LogReceiver stopped")
        raise SystemExit(0)
    
    def _check_runtime(self):
        # check path can write
        if not os.path.isdir(self.cfg.sock_path):
            raise RuntimeError("%s is not dir" % self.cfg.sock_path)
        
        if not os.access(self.cfg.sock_path, os.W_OK):
            raise RuntimeError("%s can not write")
        
        if os.path.exists(self.sock_file):
            self._d("%s existed, remove it" % self.sock_file)
            os.remove(self.sock_file)
            
    def run(self) -> None:
        d = self._d
        _pid = os.getpid()
        print("Start LogReceiver, pid=%s" % _pid)
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        self._check_runtime()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        # s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._log_sock = s
        d("Listen @ %s" % self.sock_file)
        s.bind(self.sock_file)
        # s.listen(1)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        int_size = calcsize("I")
        task_log = log_filter.LogFilter()
        
        while True:
            try:
                # this for tcp
                data, _ = s.recvfrom(65535)
                # client, client_address = s.accept()
                
                # data = client.recv(65535)
                # client.ioctl(socket.SIO_KEEPALIVE_VALS, (
                #     1,
                #     5 * 60 * 1000,
                #     5 * 60 * 1000
                # ))
                # data = client.recv(4096)
                line = data.decode()
                print("data: %s\n" % line)
                # if data.decode() == 'ping':
                #     s.sendto(b'pong', self.sock_file)
                # d("Received {0} bytes of data.".format(sys.getsizeof(data)))
            except Exception as e:
                print(e)
                continue
            # try:
            #     (i,), data = unpack("I", data[:int_size]), data[int_size:]
            # except Exception as e:
            #     print(e)
            
            # client.close()

