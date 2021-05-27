#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import multiprocessing
import time
import datetime
from libs import daemon
from libs.common import ProcessStatus
import signal
import grpc
from concurrent import futures
import libs.grpc.talent as pb2_ref
import libs.grpc.talent_pb2 as pb2
import libs.grpc.talent_pb2_grpc as pb2_grpc
from libs import db
from sqlalchemy.orm.session import Session as SqlalchemySession
import datetime


MpManagerDict = dict
_ONE_DAY = datetime.timedelta(days=1)


class TalentManager(pb2_grpc.PlotManagerServicer):
    def __init__(self, cfg):
        self.cfg: TalentCFG = cfg
    
    def get_store_dest(self, request, context):
        """
        这是一个临时函数
        
        此函数为重要的分配函数，主要用于获得下一个存储的目录。
        
        当overlord上线后此函数将丢弃
        
        :param request:
        :param context:
        :return:
        """
        ret: pb2_ref.PlotStoreDestResponse = pb2.PlotStoreDestResponse()
        ret.dest = ""
        return ret
        
    def plot_task_create(self, request, context):
        # print(request)
        ret: pb2_ref.PlotTaskStatusResponse = pb2.PlotTaskStatusResponse(type="on_create", is_success=False)
        task_id = request.task_id
        plot_config: pb2.PlotConfig = request.plot_config
        worker_id = request.worker_id
        # print(task_id, type(worker_id), type(plot_config))
        if task_id == "" \
                or worker_id == "" \
                or plot_config.ppk == "" \
                or plot_config.fpk == "" \
                or plot_config.dest.type == "" \
                or plot_config.dest.path == "" \
                or plot_config.ksize == "" \
                or plot_config.threads == "" \
                or plot_config.buffer == "" \
                or plot_config.cache1 == "":
            ret.msg = "params miss"
            return ret
        if plot_config.cache2 == "":
            plot_config.cache2 = plot_config.cache1
        session: SqlalchemySession = db.get_db_session(self.cfg.db_file)
        has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.task_id == task_id).all()
        if len(has_task) > 0:
            ret.msg = "{} already existed, please call plot_task_status(task_id) for details".format(task_id)
            # print(ret)
            return ret
        plot_task = db.DBPlotTasks()
        plot_task.worker_id = worker_id
        plot_task.task_id = task_id
        plot_task.fpk = plot_config.fpk
        plot_task.ppk = plot_config.ppk
        plot_task.ksize = plot_config.ksize
        plot_task.threads = plot_config.threads
        plot_task.buffer = plot_config.buffer
        plot_task.cache1 = plot_config.cache1
        plot_task.cache2 = plot_config.cache2
        plot_task.dest_type = plot_config.dest.type
        plot_task.dest_path = plot_config.dest.path
        plot_task.received_time = datetime.datetime.now()
        # print(plot_task)
        session.add(plot_task)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            ret.msg = str(e)
            # print("success: %s" % ret.is_success)
            # print(ret)
            return ret
        ret.is_success = True
        ret.msg = "ok"
        # print("success: %s" % ret.is_success)
        # print(ret)
        return ret
    
    def plot_task_status(self, request, context):
        session: SqlalchemySession = db.get_db_session(self.cfg.db_file)
        task_id = request.task_id
        ret: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus(task_id=task_id)
        has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.task_id == task_id).all()
        # print(has_task)
        if len(has_task) == 0:
            # print("ret: %s" % ret)
            ret.worker_id = self.cfg.worker_id
            # ret.plot_pid = 0
            # ret.log_pid = 0
            # ret.plot_details = None
            # print("ret: %s" % ret)
            return ret
        ret.existed = True
        plot_task: db.DBPlotTasks = has_task[0]
        ret.plot_pid = plot_task.plot_pid
        ret.log_pid = plot_task.log_pid
        ret.status = plot_task.status
        if type(plot_task.received_time) == datetime.datetime:
            ret.received_time = plot_task.received_time.timestamp()
        if type(plot_task.pending_time) == datetime.datetime:
            ret.pending_time = plot_task.pending_time.timestamp()
        if type(plot_task.started_time) == datetime.datetime:
            ret.started_time = plot_task.started_time.timestamp()
        if type(plot_task.running_time) == datetime.datetime:
            ret.running_time = plot_task.running_time.timestamp()
        if type(plot_task.finished_time) == datetime.datetime:
            ret.finished_time = plot_task.finished_time.timestamp()
        # print(dir(ret.plot_details))
        # print(dir(plot_task))
        for _k in dir(ret.plot_details):
            if _k[0] == "_":
                continue
            try:
                _v = getattr(plot_task, _k)
                # print("%s = %s" % (_k, _v))
                if _v:
                    ret.plot_details.__dict__[_k] = _v
            except AttributeError:
                pass
        # ret.plot_details.fpk = plot_task.fpk
        # ret.plot_details.ppk =
        # print("ret: %s" % ret)
        # todo callback overlord
        
        return ret

    def plot_task_status_all(self, request, context):
        return self._get_task_status()

    def plot_task_stop(self, request, context):
        # todo stop 需要额外一张表来追踪支持
        task_id = request.task_id
    
    def plot_task_update(self, request, context):
        _is_change = False
        request: pb2_ref.PlotTaskStatus
        session: SqlalchemySession = db.get_db_session(self.cfg.db_file)
        ret: pb2_ref.PlotTaskUpdateResponse = pb2.PlotTaskUpdateResponse()
        task_id = request.task_id
        if task_id == "":
            ret.msg = "task_id not defined"
            return ret
        has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.task_id == task_id).all()
        if len(has_task) == 0:
            ret.msg = "%s not existed" % task_id
            return ret
        plot_task: db.DBPlotTasks = has_task[0]
        if request.plot_pid != 0:
            _is_change = True
            plot_task.plot_pid = request.plot_pid
        if request.log_pid != 0:
            _is_change = True
            plot_task.log_pid = request.log_pid
        if request.status != "":
            _is_change = True
            plot_task.status = request.status
        if request.remarks != "":
            _is_change = True
            plot_task.remarks = request.remarks
        # todo 2021-05-24 finish 未全面测试
        if request.pending_time != 0.0:
            _is_change = True
            plot_task.pending_time = datetime.datetime.fromtimestamp(request.pending_time)
        if request.started_time != 0.0:
            _is_change = True
            plot_task.started_time = datetime.datetime.fromtimestamp(request.started_time)
        if request.running_time != 0.0:
            _is_change = True
            plot_task.running_time = datetime.datetime.fromtimestamp(request.running_time)
        if request.finished_time != 0.0:
            _is_change = True
            plot_task.finished_time = datetime.datetime.fromtimestamp(request.finished_time)
            
        if request.plot_details.fpk != "":
            _is_change = True
            plot_task.fpk = request.plot_details.fpk
        if request.plot_details.ppk != "":
            _is_change = True
            plot_task.ppk = request.plot_details.ppk
        if request.plot_details.ksize != 0:
            _is_change = True
            plot_task.ksize = request.plot_details.ksize
        if request.plot_details.cache1 != "":
            _is_change = True
            plot_task.cache1 = request.plot_details.cache1
        if request.plot_details.cache2 != "":
            _is_change = True
            plot_task.cache2 = request.plot_details.cache2
        if request.plot_details.buffer != 0:
            _is_change = True
            plot_task.buffer = request.plot_details.buffer
        if request.plot_details.buckets != 0:
            _is_change = True
            plot_task.buckets = request.plot_details.buckets
        if request.plot_details.threads != 0:
            _is_change = True
            plot_task.threads = request.plot_details.threads
        if request.plot_details.stripe_size != 0:
            _is_change = True
            plot_task.stripe_size = request.plot_details.stripe_size
        if request.plot_details.memo != "":
            _is_change = True
            plot_task.memo = request.plot_details.memo
        if request.plot_details.progress != 0.0:
            _is_change = True
            plot_task.progress = request.plot_details.progress
        if request.plot_details.stage_now != 0:
            _is_change = True
            plot_task.stage_now = request.plot_details.stage_now
        if request.plot_details.dest_type != "":
            _is_change = True
            plot_task.dest_type = request.plot_details.dest_type
        if request.plot_details.dest_path != "":
            _is_change = True
            plot_task.dest_path = request.plot_details.dest_path
        if request.plot_details.dest_file_name != "":
            _is_change = True
            plot_task.dest_file_name = request.plot_details.dest_file_name
            
        # phase 1 detail
        if request.plot_details.phase_1_status.t1.time != 0.0:
            _is_change = True
            plot_task.p1_t1_time = request.plot_details.phase_1_status.t1.time
        if request.plot_details.phase_1_status.t1.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t1_cpu = request.plot_details.phase_1_status.t1.cpu_usage
        
        if request.plot_details.phase_1_status.t2.time != 0.0:
            _is_change = True
            plot_task.p1_t2_time = request.plot_details.phase_1_status.t2.time
        if request.plot_details.phase_1_status.t2.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t2_cpu = request.plot_details.phase_1_status.t2.cpu_usage

        if request.plot_details.phase_1_status.t3.time != 0.0:
            _is_change = True
            plot_task.p1_t3_time = request.plot_details.phase_1_status.t3.time
        if request.plot_details.phase_1_status.t3.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t3_cpu = request.plot_details.phase_1_status.t3.cpu_usage

        if request.plot_details.phase_1_status.t4.time != 0.0:
            _is_change = True
            plot_task.p1_t4_time = request.plot_details.phase_1_status.t4.time
        if request.plot_details.phase_1_status.t4.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t4_cpu = request.plot_details.phase_1_status.t4.cpu_usage

        if request.plot_details.phase_1_status.t5.time != 0.0:
            _is_change = True
            plot_task.p1_t5_time = request.plot_details.phase_1_status.t5.time
        if request.plot_details.phase_1_status.t5.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t5_cpu = request.plot_details.phase_1_status.t5.cpu_usage

        if request.plot_details.phase_1_status.t6.time != 0.0:
            _is_change = True
            plot_task.p1_t6_time = request.plot_details.phase_1_status.t6.time
        if request.plot_details.phase_1_status.t6.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t6_cpu = request.plot_details.phase_1_status.t6.cpu_usage

        if request.plot_details.phase_1_status.t7.time != 0.0:
            _is_change = True
            plot_task.p1_t7_time = request.plot_details.phase_1_status.t7.time
        if request.plot_details.phase_1_status.t7.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_t7_cpu = request.plot_details.phase_1_status.t7.cpu_usage
        
        # p1 total
        if request.plot_details.phase_1_status.time != 0.0:
            _is_change = True
            plot_task.p1_total_time = request.plot_details.phase_1_status.time
        if request.plot_details.phase_1_status.cpu_usage != 0.0:
            _is_change = True
            plot_task.p1_total_cpu = request.plot_details.phase_1_status.cpu_usage

        # p2
        if request.plot_details.phase_2_status.t1.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t1_scan_time = request.plot_details.phase_2_status.t1.scan.time
        if request.plot_details.phase_2_status.t1.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t1_scan_cpu = request.plot_details.phase_2_status.t1.scan.cpu_usage
        if request.plot_details.phase_2_status.t1.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t1_sort_time = request.plot_details.phase_2_status.t1.sort.time
        if request.plot_details.phase_2_status.t1.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t1_sort_cpu = request.plot_details.phase_2_status.t1.sort.cpu_usage

        if request.plot_details.phase_2_status.t2.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t2_scan_time = request.plot_details.phase_2_status.t2.scan.time
        if request.plot_details.phase_2_status.t2.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t2_scan_cpu = request.plot_details.phase_2_status.t2.scan.cpu_usage
        if request.plot_details.phase_2_status.t2.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t2_sort_time = request.plot_details.phase_2_status.t2.sort.time
        if request.plot_details.phase_2_status.t2.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t2_sort_cpu = request.plot_details.phase_2_status.t2.sort.cpu_usage

        if request.plot_details.phase_2_status.t3.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t3_scan_time = request.plot_details.phase_2_status.t3.scan.time
        if request.plot_details.phase_2_status.t3.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t3_scan_cpu = request.plot_details.phase_2_status.t3.scan.cpu_usage
        if request.plot_details.phase_2_status.t3.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t3_sort_time = request.plot_details.phase_2_status.t3.sort.time
        if request.plot_details.phase_2_status.t3.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t3_sort_cpu = request.plot_details.phase_2_status.t3.sort.cpu_usage

        if request.plot_details.phase_2_status.t4.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t4_scan_time = request.plot_details.phase_2_status.t4.scan.time
        if request.plot_details.phase_2_status.t4.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t4_scan_cpu = request.plot_details.phase_2_status.t4.scan.cpu_usage
        if request.plot_details.phase_2_status.t4.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t4_sort_time = request.plot_details.phase_2_status.t4.sort.time
        if request.plot_details.phase_2_status.t4.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t4_sort_cpu = request.plot_details.phase_2_status.t4.sort.cpu_usage

        if request.plot_details.phase_2_status.t5.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t5_scan_time = request.plot_details.phase_2_status.t5.scan.time
        if request.plot_details.phase_2_status.t5.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t5_scan_cpu = request.plot_details.phase_2_status.t5.scan.cpu_usage
        if request.plot_details.phase_2_status.t5.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t5_sort_time = request.plot_details.phase_2_status.t5.sort.time
        if request.plot_details.phase_2_status.t5.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t5_sort_cpu = request.plot_details.phase_2_status.t5.sort.cpu_usage

        if request.plot_details.phase_2_status.t6.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t6_scan_time = request.plot_details.phase_2_status.t6.scan.time
        if request.plot_details.phase_2_status.t6.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t6_scan_cpu = request.plot_details.phase_2_status.t6.scan.cpu_usage
        if request.plot_details.phase_2_status.t6.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t6_sort_time = request.plot_details.phase_2_status.t6.sort.time
        if request.plot_details.phase_2_status.t6.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t6_sort_cpu = request.plot_details.phase_2_status.t6.sort.cpu_usage

        if request.plot_details.phase_2_status.t7.scan.time != 0.0:
            _is_change = True
            plot_task.p2_t7_scan_time = request.plot_details.phase_2_status.t7.scan.time
        if request.plot_details.phase_2_status.t7.scan.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t7_scan_cpu = request.plot_details.phase_2_status.t7.scan.cpu_usage
        if request.plot_details.phase_2_status.t7.sort.time != 0.0:
            _is_change = True
            plot_task.p2_t7_sort_time = request.plot_details.phase_2_status.t7.sort.time
        if request.plot_details.phase_2_status.t7.sort.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_t7_sort_cpu = request.plot_details.phase_2_status.t7.sort.cpu_usage

        # p2 total
        if request.plot_details.phase_2_status.time != 0.0:
            _is_change = True
            plot_task.p2_total_time = request.plot_details.phase_2_status.time
        if request.plot_details.phase_2_status.cpu_usage != 0.0:
            _is_change = True
            plot_task.p2_total_cpu = request.plot_details.phase_2_status.cpu_usage
            
        # phase 3 detail
        if request.plot_details.phase_3_status.t1_2.time != 0.0:
            _is_change = True
            plot_task.p3_t1_2_time = request.plot_details.phase_3_status.t1_2.time
        if request.plot_details.phase_3_status.t1_2.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t1_2_cpu = request.plot_details.phase_3_status.t1_2.cpu_usage

        if request.plot_details.phase_3_status.t2_3.time != 0.0:
            _is_change = True
            plot_task.p3_t2_3_time = request.plot_details.phase_3_status.t2_3.time
        if request.plot_details.phase_3_status.t2_3.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t2_3_cpu = request.plot_details.phase_3_status.t2_3.cpu_usage

        if request.plot_details.phase_3_status.t3_4.time != 0.0:
            _is_change = True
            plot_task.p3_t3_4_time = request.plot_details.phase_3_status.t3_4.time
        if request.plot_details.phase_3_status.t3_4.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t3_4_cpu = request.plot_details.phase_3_status.t3_4.cpu_usage

        if request.plot_details.phase_3_status.t4_5.time != 0.0:
            _is_change = True
            plot_task.p3_t4_5_time = request.plot_details.phase_3_status.t4_5.time
        if request.plot_details.phase_3_status.t4_5.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t4_5_cpu = request.plot_details.phase_3_status.t4_5.cpu_usage

        if request.plot_details.phase_3_status.t5_6.time != 0.0:
            _is_change = True
            plot_task.p3_t5_6_time = request.plot_details.phase_3_status.t5_6.time
        if request.plot_details.phase_3_status.t5_6.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t5_6_cpu = request.plot_details.phase_3_status.t5_6.cpu_usage

        if request.plot_details.phase_3_status.t6_7.time != 0.0:
            _is_change = True
            plot_task.p3_t6_7_time = request.plot_details.phase_3_status.t6_7.time
        if request.plot_details.phase_3_status.t6_7.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_t6_7_cpu = request.plot_details.phase_3_status.t6_7.cpu_usage
        
        # p3 total
        if request.plot_details.phase_3_status.time != 0.0:
            _is_change = True
            plot_task.p3_total_time = request.plot_details.phase_3_status.time
        if request.plot_details.phase_3_status.cpu_usage != 0.0:
            _is_change = True
            plot_task.p3_total_cpu = request.plot_details.phase_3_status.cpu_usage
        
        # p4 total
        if request.plot_details.phase_4_status.time != 0.0:
            _is_change = True
            plot_task.p4_total_time = request.plot_details.phase_4_status.time
        if request.plot_details.phase_4_status.cpu_usage != 0.0:
            _is_change = True
            plot_task.p4_total_cpu = request.plot_details.phase_4_status.cpu_usage

        # total
        if request.plot_details.total_time.time != 0.0:
            _is_change = True
            plot_task.total_time = request.plot_details.total_time.time

        if request.plot_details.total_time.cpu_usage != 0.0:
            _is_change = True
            plot_task.total_cpu = request.plot_details.total_time.cpu_usage
        
        # copy
        if request.plot_details.copy_time.time != 0.0:
            _is_change = True
            plot_task.copy_time = request.plot_details.copy_time.time
        
        if request.plot_details.copy_time.cpu_usage != 0.0:
            _is_change = True
            plot_task.copy_cpu = request.plot_details.copy_time.cpu_usage

        # todo 2021-05-24 finish need test over
        
        if _is_change:
            session.add(plot_task)
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                ret.msg = str(e)
                # print("success: %s" % ret.is_success)
                # print(ret)
                return ret
        
            ret.is_success = True
            ret.msg = "ok"
        else:
            ret.msg = "no change"
        return ret
    
    def get_plot_tasks(self, request, context):
        if request.status == "":
            _status = 'received'
        else:
            _status = request.status
        return self._get_task_status(status=_status)
    
    def get_plot_by_cache(self, request: pb2_ref.GetPlotByCacheRequest, context):
        if request.status != "":
            _status = request.status
        else:
            _status = "running"
        if request.cache1 == "":
            raise RuntimeError("cache1 not defined")
        return self._get_task_status(_status, request.cache1)
        
    def _get_task_status(self, status=None, cache1=None):
        """
        返回指定状态的数据，如果没有指定状态，则返回当前数据库中所有数据
        
        :param status: [received, pending, started, running, finished]
        :return:
        """
        session: SqlalchemySession = db.get_db_session(self.cfg.db_file)
        ret: pb2_ref.PlotTaskStatusAllResponse = pb2.PlotTaskStatusAllResponse()
        
        if status is not None and cache1 is None:
            has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.status == status).all()
        elif status is None and cache1 is not None:
            has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.cache1 == cache1).all()
        elif status is not None and cache1 is not None:
            has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.status == status).filter(db.DBPlotTasks.cache1 == cache1).all()
        else:
            has_task = session.query(db.DBPlotTasks).all()
        
        _t: db.DBPlotTasks
        for _t in has_task:
            _ret: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
            _ret.task_id = _t.task_id
            _ret.worker_id = _t.worker_id
            _ret.existed = True
            _ret.plot_pid = _t.plot_pid
            _ret.log_pid = _t.log_pid
            _ret.status = _t.status
            if type(_t.received_time) == datetime.datetime:
                _ret.received_time = _t.received_time.timestamp()
            if type(_t.pending_time) == datetime.datetime:
                _ret.pending_time = _t.pending_time.timestamp()
            if type(_t.started_time) == datetime.datetime:
                _ret.started_time = _t.started_time.timestamp()
            if type(_t.running_time) == datetime.datetime:
                _ret.running_time = _t.running_time.timestamp()
            if type(_t.finished_time) == datetime.datetime:
                _ret.finished_time = _t.finished_time.timestamp()
            # print(dir(ret.plot_details))
            for _k in dir(_ret.plot_details):
                if _k[0] == "_":
                    continue
                try:
                    _v = getattr(_t, _k)
                    # print("%s = %s" % (_k, _v))
                    if _v:
                        _ret.plot_details.__dict__[_k] = _v
                except AttributeError:
                    pass
            ret.tasks.append(_ret)
        return ret
        

class TalentCFG(object):
    db_file: str = "/tmp/owl/talent.db"
    worker_id: str = "server1"
    overlord: str = "192.168.1.100"
    grpc_port: int = 50051


class Talent(multiprocessing.Process):
    """
    Talent 是负责与
    """
    _manager: MpManagerDict = None
    _app_cfg: TalentCFG
    _app_status: ProcessStatus
    _rpc_server = None
    # prometheus_host = "127.0.0.1"
    
    def __init__(self, cfg: TalentCFG, manager: MpManagerDict = None, debug: bool = False, *args, **kwargs):
        self.cfg = cfg
        self._debug = debug
        if manager is not None:
            self._manager = manager

        # print("Start Success")
        # daemon.output_to_log(stdout='/tmp/glue_stdout.log', stderr='/tmp/glue_stderr.log')
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
        print('PID:%s Talent 收到退出请求' % os.getpid())
        sys.stdout.flush()
        print("Talent stopping grpc server")
        self._rpc_server.stop(grace=30)
        raise SystemExit(0)
    
    def run(self):
        d = self._d
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        d('Talent 初始化启动')
        self._app_check()
        self._rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        pb2_grpc.add_PlotManagerServicer_to_server(TalentManager(self.cfg), self._rpc_server)
        self._rpc_server.add_insecure_port('[::]:%s' % self.cfg.grpc_port)
        self._rpc_server.start()
    
        while True:
            time.sleep(_ONE_DAY.total_seconds())
        

