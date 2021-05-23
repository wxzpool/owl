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


MpManagerDict = dict
_ONE_DAY = datetime.timedelta(days=1)


class TalentManager(pb2_grpc.PlotManagerServicer):
    def __init__(self, cfg):
        self.cfg: TalentCFG = cfg
        
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
                or plot_config.cache1 == "" \
                or plot_config.cache2 == "":
            ret.msg = "params miss"
            return ret
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
        plot_task = has_task[0]
        if request.plot_pid != 0:
            _is_change = True
            plot_task.plot_pid = request.plot_pid
        if request.log_pid != 0:
            _is_change = True
            plot_task.log_pid = request.log_pid
        if request.status != "":
            _is_change = True
            plot_task.status = request.status
        # todo 2021-05-23 not finish
        
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
        _status = 'received'
        return self._get_task_status(status=_status)
        
    def _get_task_status(self, status=None):
        session: SqlalchemySession = db.get_db_session(self.cfg.db_file)
        ret: pb2_ref.PlotTaskStatusAllResponse = pb2.PlotTaskStatusAllResponse()
        if status is None:
            has_task = session.query(db.DBPlotTasks).all()
        else:
            has_task = session.query(db.DBPlotTasks).filter(db.DBPlotTasks.status == status).all()
        _t: db.DBPlotTasks
        for _t in has_task:
            _ret: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
            _ret.task_id = _t.task_id
            _ret.worker_id = _t.worker_id
            _ret.existed = True
            _ret.plot_pid = _t.plot_pid
            _ret.log_pid = _t.log_pid
            _ret.status = _t.status
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
        self._rpc_server.add_insecure_port('[::]:50051')
        self._rpc_server.start()
    
        while True:
            time.sleep(_ONE_DAY.total_seconds())
        

