#!/usr/bin/env python3
# encoding: utf-8
# 每个p图进程都会对应一个日志收集人，收集到的日志会统一通讯给talent并由talent上传给octopus
import multiprocessing
# import threading
from libs.sturcts import ProcessStatus
import os
import sys
import time
import signal
from struct import unpack, calcsize
import socket
from . import log_filter
import grpc
from .grpc import talent_pb2 as pb2
from .grpc import talent_pb2_grpc as pb2_grpc
from .grpc import talent as pb2_ref


MpManagerDict = dict


class LogReceiverCFG(object):
    task_id: str
    name: str
    sock_path: str
    log_store: str
    grpc_host: str = "127.0.0.1:50051"


class LogReceiver(multiprocessing.Process):
    # class LogReceiver(threading.Thread):
    # todo LogReceiver 作为单独的脚本，重写
    _app_cfg: LogReceiverCFG
    _manager: MpManagerDict = None
    _app_status: ProcessStatus
    _log_sock = None
    store: pb2.PlotTaskUpdateResponse
    # pid: int

    def __init__(self, cfg: LogReceiverCFG, manager: MpManagerDict = None, debug: bool = False, *args, **kwargs):
        self.cfg = cfg
        self._debug = debug
        self.sock_file = "%s/%s.sock" % (self.cfg.sock_path, self.cfg.name)
        if manager is not None:
            self._manager = manager
        # print("LogReceiver Start Success")
        super().__init__(*args, **kwargs)

    def _d(self, msg):
        _name = "LogReceiver-%s" % self.cfg.name
        _pid = os.getpid()
        _now = time.time()
        # print('[%s]-[PID: %d]-[%.3f] %s' % (_name, _pid, _now, msg))
        if self._debug:
            with open("%s/log_receiver-%s.log" % (self.cfg.log_store, self.cfg.name), "a") as log:
                log.write('[PID: %d] [%.3f] %s\n' % (_pid, _now, msg))
                log.flush()
    
    def terminate(self, *args, **kwargs):
        self._d('PID:%s LogReceiver收到退出请求' % self.pid)
        sys.stdout.flush()
        if self._log_sock is not None:
            self._log_sock.close()
        try:
            os.remove(self.sock_file)
        except (OSError, FileNotFoundError):
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

    def _update_task(self, task_status: pb2_ref.PlotTaskStatus) -> pb2_ref.PlotTaskUpdateResponse:
        d = self._d
        resp: pb2_ref.PlotTaskUpdateResponse
        try:
            with grpc.insecure_channel(self.cfg.grpc_host) as channel:
                stub = pb2_grpc.PlotManagerStub(channel)
                resp = stub.plot_task_update(task_status)
        except grpc.RpcError as e:
            d("RPC Error, ignore, err: %s" % e)
        return resp
        
    def run(self) -> None:
        d = self._d
        # self.pid = os.getpid()
        d("Start LogReceiver, pid=%s" % self.pid)
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        self._check_runtime()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        # s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._log_sock = s
        d("Listen @ %s" % self.sock_file)
        s.bind(self.sock_file)
        # atexit.register(lambda: os.remove(self.sock_file))
        # s.listen(1)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        int_size = calcsize("I")
        plot_task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
        plot_task_status.task_id = self.cfg.task_id
        # plot_task_status.status = "running"
        task_log = log_filter.LogFilter(plot_task_status)
        # self._update_task(task_log.get_status())
        
        while True:
            try:
                # this for tcp
                _is_change = False
                data, _ = s.recvfrom(65535)
                # client, client_address = s.accept()
                
                # data = client.recv(65535)
                # client.ioctl(socket.SIO_KEEPALIVE_VALS, (
                #     1,
                #     5 * 60 * 1000,
                #     5 * 60 * 1000
                # ))
                # data = client.recv(4096)
                lines = data.decode()
                for line in lines.split("\n"):
                    
                    # d("data: %s" % line)
                    # d("find data: %s\n" % task_log.parser(line))
                    if task_log.parser(line):
                        _is_change = True
                # d('结果: \n')
                
                # if data.decode() == 'ping':
                #     s.sendto(b'pong', self.sock_file)
                # d("Received {0} bytes of data.".format(sys.getsizeof(data)))
                if _is_change:
    
                    self._update_task(task_log.get_status())

                    # for _k in dir(self.store):
                    #     if _k[0] == "_":
                    #         continue
                    #     try:
                    #         _v = getattr(self.store, _k)
                    #         d("%s = %s" % (_k, _v))
                    #     except AttributeError:
                    #         pass
                # d("\n")
            except Exception as e:
                d(e)
                continue
            # try:
            #     (i,), data = unpack("I", data[:int_size]), data[int_size:]
            # except Exception as e:
            #     print(e)
            
            # client.close()
