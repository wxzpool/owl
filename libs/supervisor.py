#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
# import multiprocessing
import time
from libs.sturcts import ProcessStatus, CacheCFG, PlotProcessCFG, SupervisorCFG
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
from .common import get_ksize_capacity
import psutil

MpManagerDict = dict


class ProcessList(object):
    task_id: str
    cfg: PlotterCFG
    plotter: Plotter
    logger: LogReceiver


# class Supervisor(multiprocessing.Process):
class Supervisor(object):
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
        if 'pid' in kwargs:
            self.pid = kwargs['pid']
        # print("Start Success")
        # daemon.output_to_log(stdout='/tmp/glue_stdout.log', stderr='/tmp/glue_stderr.log')
        
        # super().__init__(*args, **kwargs)
    
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
        _name = "Supervisor"
        _pid = os.getpid()
        _now = time.time()
        if self._debug:
            print('[%s]-[PID: %d]-[%.3f] %s' % (_name, _pid, _now, msg))
        with open(self.cfg.log_file, "a") as log:
            log.write('[PID: %d] [%.3f] %s\n' % (_pid, _now, msg))
            log.flush()
    
    def _start_sock_logger(self, task_id, sock_path, log_store) -> LogReceiver:
        logger_cfg = LogReceiverCFG()
        logger_cfg.name = task_id
        logger_cfg.task_id = task_id
        logger_cfg.sock_path = sock_path
        logger_cfg.log_store = log_store
        logger_cfg.grpc_host = self.cfg.grpc_host
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
        d = self._d
        ret: [PlotterCFG] = list()
        # 返回的是一个PlotProcessCFG元素的数组
        _get_err = True
        while _get_err:
            try:
                with grpc.insecure_channel(self.cfg.grpc_host) as channel:
                    # d("获取所有状态为{}的记录".format(status))
                    stub = pb2_grpc.PlotManagerStub(channel)
                    resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(pb2.PlotStatus(status=status))
                    _get_err = False
            except grpc.RpcError as e:
                d("RPC Error, try again after 10 sec")
                d(e)
                time.sleep(10)
        for task in resp.tasks:
            plot_cfg = PlotterCFG()
            plot_cfg.log_store = self.cfg.plot_process_config.log_store
            plot_cfg.bin = self.cfg.plot_process_config.bin
            plot_cfg.python = self.cfg.plot_process_config.python
            # plot_cfg.cache1 = self.cfg.plot_process_config.cache1
            # plot_cfg.cache2 = self.cfg.plot_process_config.cache2
            plot_cfg.name = task.task_id
            plot_cfg.task_id = task.task_id
            plot_cfg.fpk = task.plot_details.fpk
            # d(task.plot_details.fpk)
            plot_cfg.ppk = task.plot_details.ppk
            plot_cfg.thread = task.plot_details.threads
            plot_cfg.mem = task.plot_details.buffer
            plot_cfg.cache1 = task.plot_details.cache1
            # d(task.plot_details.cache1)
            plot_cfg.cache2 = task.plot_details.cache2
            plot_cfg.dest = task.plot_details.dest_path
            plot_cfg.ksize = task.plot_details.ksize
            
            ret.append(plot_cfg)
        return ret
    
    def _update_task(self, task_status: pb2_ref.PlotTaskStatus) -> pb2_ref.PlotTaskUpdateResponse:
        _get_err = True
        d = self._d
        while _get_err:
            try:
                with grpc.insecure_channel(self.cfg.grpc_host) as channel:
                    stub = pb2_grpc.PlotManagerStub(channel)
                    resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(task_status)
                    _get_err = False
            except grpc.RpcError as e:
                d("RPC Error, try again after 10 sec")
                d(e)
                time.sleep(10)
        return resp

    def terminate(self, *args, **kwargs):
        d = self._d
        d('PID:%s Supervisor 收到退出请求' % os.getpid())
        sys.stdout.flush()
        # 关闭log
        # logger = self._logger
        # if logger.is_alive():
        #    os.kill(logger.pid, signal.SIGTERM)
        # todo Supervisor管理了多个的p图进程，需要遍历并关闭他们
        for pl in self._process_list:
            d("%s关闭子进程plotter: %s, logger: %s" % (pl.task_id, pl.plotter.pid, pl.logger.pid))
            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
            task_status.task_id = pl.task_id
            task_status.status = "stopped"
            self._update_task(task_status)
            # pl.plotter.terminate()
            try:
                os.kill(pl.plotter.pid, signal.SIGKILL)
                os.kill(pl.logger.pid, signal.SIGTERM)
                pl.plotter.join()
                pl.logger.join()
            except ProcessLookupError:
                pass
        d("Supervisor stopped")
        raise SystemExit(0)
    
    def _count_cache1_task(self, cache1) -> int:
        _c = 0
        for _p in self._process_list:
            if cache1 == _p.cfg.cache1:
                _c += 1
        return _c
    
    def run(self):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d = self._d
        _pid = os.getpid()
        d("Start Supervisor, pid=%s" % _pid)
        self._check_runtime()
        while True:
            # 2021-06-04 进程经常自己退出，捕捉全部的error
            try:
                # 检查现有任务状态
                d("当前任务数量: %s" % len(self._process_list))
                for _i, pl in enumerate(self._process_list):
                    # todo 监控进程是否退出
                    # d("I: %s" % _i)
                    # d("plot task: %s = %s" % (pl.plotter.pid, pl.plotter.is_alive()))
                    # d("log task: %s = %s" % (pl.logger.pid, pl.logger.is_alive()))
                    # d("\n")
                    if not pl.plotter.is_alive():
                        d("plotter no existed, remove logger, remove work list")
                        os.kill(pl.logger.pid, signal.SIGTERM)
                        del self._process_list[_i]
                # 定时获取任务， grpc调用talent
                # 应该先执行所有pending的任务
                for _status in ["pending", "received"]:
                    _all_tasks = self._get_task(_status)
                    d("%s状态数量: %s" % (_status, len(_all_tasks)))
                    for t in _all_tasks:
                        d("Task: %s" % t.task_id)
                        # d("Cache1: %s" % t.cache1)
                        # d(t.bin)
                        # d(t.cache1)
                        # 机器应该有最大上限(按照ssd划分)
                        # todo cache2 暂时不支持
                        # print(t.cache1)
                        # 2021-06-06 ssd 容量使用psutil获得
                        # ssd_capacity = self.cfg.plot_process_config.get_cache1_info(t.cache1)
                        try:
                            ssd_usage = psutil.disk_usage(t.cache1)
                        except FileNotFoundError:
                            # d("ssd 容量: %s" % ssd_capacity)
                            # 无法获取ssd容量会引起错误，回写状态
                            # if ssd_capacity == 0:
                            d("无法获取ssd(%s)容量" % t.cache1)
                            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                            task_status.task_id = t.task_id
                            task_status.status = "failed"
                            task_status.remarks = "无法获取ssd(%s)容量" % t.cache1
                            # d(task_status.remarks)
                            res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                            # d("callback, is_success:{}, msg: {}".format(
                            #     res.is_success,
                            #     res.msg
                            # ))
                            continue
                        ssd_capacity = ssd_usage.total / 1024 / 1024
                        # with grpc.insecure_channel(self.cfg.grpc_host) as channel:
                        #     # d("首先获取当前所有状态为{}，cache1为{}上的进程".format(
                        #     #     "running",
                        #     #     t.cache1
                        #     # ))
                        #     stub = pb2_grpc.PlotManagerStub(channel)
                        #     request: pb2_ref.GetPlotByCacheRequest = pb2.GetPlotByCacheRequest()
                        #     request.status = "running"
                        #     request.cache1 = t.cache1
                        #     resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(request)
                        # 返回获取运行数量
                        running_number = self._count_cache1_task(t.cache1)
                        ksize_capacity = get_ksize_capacity(t.ksize)
                        # print(ksize_capacity)
                        max_proc = round(ssd_capacity / ksize_capacity)
                        d("%s MAX: %s" % (t.cache1, max_proc))
                        if running_number >= max_proc:
                            d("达到ssd最大进程数，任务pending")
                            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                            task_status.task_id = t.task_id
                            task_status.status = "pending"
                            task_status.remarks = "达到ssd最大进程数，任务pending"
                            task_status.pending_time = time.time()
                            res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                            # d("callback, is_success:{}, msg: {}".format(
                            #     res.is_success,
                            #     res.msg
                            # ))
                            continue
                        # 2021-06-06 增加最终目标容量判断
                        _dest = t.dest
                        try:
                            _dest_usage = psutil.disk_usage(_dest)
                        except FileNotFoundError:
                            _msg = "无法获得%s的容量" % _dest
                            d(_msg)
                            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                            task_status.task_id = t.task_id
                            task_status.status = 'failed'
                            task_status.remarks = _msg
                            res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                            continue
                        if _dest_usage.percent > self.cfg.plot_process_config.cap_limit:
                            _total = round(_dest_usage.total / 1024 / 1024 / 1024 / 1024, 2)
                            _free = round(_dest_usage.free / 1024 / 1024 / 1024 / 1024, 2)
                            _msg = "使用容量超过阈值 {a} > {b}, dest: {dest}, total: {total}, free: {free}".format(
                                a=_dest_usage.percent,
                                b=self.cfg.plot_process_config.cap_limit,
                                dest=_dest,
                                total=_total,
                                free=_free
                            )
                            d(_msg)
                            task_status: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
                            task_status.task_id = t.task_id
                            task_status.status = 'failed'
                            task_status.remarks = _msg
                            res: pb2_ref.PlotTaskUpdateResponse = self._update_task(task_status)
                            continue
                        process = ProcessList()
                        process.cfg = t
                        process.task_id = t.task_id
                        # print("start logger")
                        process.logger = self._start_sock_logger(t.task_id, self.cfg.sock_path, self.cfg.plot_process_config.log_store)
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
                        task_status.started_time = time.time()
                        task_status.remarks = "任务开始"
                        self._update_task(task_status)
                    # 然后获取最新状态为received的任务，并执行
                    # todo not test
                # sleep and run again
                time.sleep(self.cfg.sleep_time)
            except Exception as e:
                raise e
                # import traceback
                # d("GET ERROR: %s" % traceback.print_tb(e))
                # d("Trace frame: %s" % e.__traceback__.tb_frame)
                # d("Trace line: %s" % e.__traceback__.tb_lineno)
            

        
        
        
        
        

