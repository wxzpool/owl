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
import time
import socket
import grpc
import libs.grpc.talent as pb2_ref
import libs.grpc.talent_pb2 as pb2
import libs.grpc.talent_pb2_grpc as pb2_grpc
from libs.common import get_ksize_capacity

MpManagerDict = dict


class ProcessList(object):
    task_id: str
    plotter: Plotter
    logger: LogReceiver


class CacheCFG(object):
    dest: str
    capacity: int


class PlotProcessCFG(object):
    bin: str = "/tmp/chia"
    waiting: int = 1200
    cache1: [CacheCFG]
    cache2: [CacheCFG]
    dests: [str]
    
    def get_cache1_info(self, t):
        for c in self.cache1:
            if t == c.dest:
                return t
        return None


class SupervisorCFG(object):
    sock_path: str = "/tmp"
    grpc_host: str = "127.0.0.1:50051"
    sleep_time: int = 10
    plot_process_config: PlotProcessCFG
    
    
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
        # todo 启动时候应该检查任务状态，是否有异常任务
    
    def _get_task(self, status) -> [PlotterCFG]:
        ret: [PlotterCFG] = list()
        # 返回的是一个PlotProcessCFG元素的数组
        with grpc.insecure_channel(self.cfg.grpc_host) as channel:
            print("获取所有状态为{}的记录".format(status))
            stub = pb2_grpc.PlotManagerStub(channel)
            resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(pb2.PlotStatus(status=status))
        for task in resp.tasks:
            plot_cfg = PlotterCFG()
            plot_cfg.task_id = task.task_id
            plot_cfg.fpk = task.plot_details.fpk
            plot_cfg.ppk = task.plot_details.ppk
            plot_cfg.thread = task.plot_details.threads
            plot_cfg.mem = task.plot_details.buffer
            plot_cfg.cache1 = task.plot_details.cache1
            plot_cfg.cache2 = task.plot_details.cache2
            plot_cfg.dest = task.plot_details.dest_path
            plot_cfg.ksize = task.plot_details.ksize
            ret.append(plot_cfg)
        return ret
    
    def _update_task(self, task_status: pb2_ref.PlotTaskStatus) -> pb2_ref.PlotTaskUpdateResponse:
        with grpc.insecure_channel(self.cfg.grpc_host) as channel:
            stub = pb2_grpc.PlotManagerStub(channel)
            resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(task_status)
        return resp

    def terminate(self, *args, **kwargs):
        d = self._d
        print('PID:%s Supervisor 收到退出请求' % os.getpid())
        sys.stdout.flush()
        # 关闭log
        # logger = self._logger
        # if logger.is_alive():
        #    os.kill(logger.pid, signal.SIGTERM)
        # todo Supervisor管理了多个的p图进程，需要遍历并关闭他们
        for pl in self._process_list:
            print("%s关闭子进程plotter: %s, logger: %s" % (pl.task_id, pl.plotter.pid, pl.logger.pid))
            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
            task_status.task_id = pl.task_id
            task_status.status = "stopped"
            self._update_task(task_status)
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
            # todo 监控进程是否退出
            d(pl.plotter.pid)
        # 定时获取任务， grpc调用talent
        # 应该先执行所有pending的任务
        for _status in ["pending", "received"]:
            for t in self._get_task(_status):
                # todo 机器应该有最大上限(按照ssd划分)
                ssd_capacity = self.cfg.plot_process_config.get_cache1_info(t.cache1)
                # 无法获取ssd容量会引起错误，回写状态
                if ssd_capacity == 0:
                    print("无法获取ssd(%s)容量" % t.cache1)
                    task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                    task_status.task_id = t.task_id
                    task_status.status = "failed"
                    task_status.remarks = "无法获取ssd(%s)容量" % t.cache1
                    print(task_status.remarks)
                    res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                    print("callback, is_success:{}, msg: {}".format(
                        res.is_success,
                        res.msg
                    ))
                    continue
                    
                with grpc.insecure_channel(self.cfg.grpc_host) as channel:
                    print("首先获取当前所有状态为{}，cache1为{}上的进程".format(
                        "running",
                        t.cache1
                    ))
                    stub = pb2_grpc.PlotManagerStub(channel)
                    request: pb2_ref.GetPlotByCacheRequest = pb2.GetPlotByCacheRequest()
                    request.status = "running"
                    request.cache1 = t.cache1
                    resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(request)
                # 返回获取运行数量
                running_number = len(resp.tasks)
                ksize_capacity = get_ksize_capacity(t.ksize)
                max_proc = round(ssd_capacity / ksize_capacity)
                if running_number >= max_proc:
                    task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                    request.task_id = t.task_id
                    task_status.remarks = "达到ssd最大进程数，任务pending"
                    res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                    print("callback, is_success:{}, msg: {}".format(
                        res.is_success,
                        res.msg
                    ))
                    continue
                
                process = ProcessList()
                process.task_id = t.task_id
                # print("start logger")
                process.logger = self._start_sock_logger(t.name, self.cfg.sock_path)
                d(process.logger)
                # time.sleep(3)
                # test sock server up
                task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                task_status.task_id = t.task_id
                task_status.log_pid = process.logger.pid
                self._update_task(task_status)
                while True:
                    if os.path.exists(process.logger.sock_file):
                        break
                    time.sleep(1)
                # print("start plotter")
                process.plotter = self._start_plotter(t, process.logger.sock_file)
                d(process.plotter)
                self._process_list.append(process)
                task_status.plot_pid = process.plotter.pid
                task_status.status = "started"
                self._update_task(task_status)
            # 然后获取最新状态为received的任务，并执行
            # todo not test
        # sleep and run again
        time.sleep(self.cfg.sleep_time)
            

        
        
        
        
        

