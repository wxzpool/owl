#!/usr/bin/env python3
# encoding: utf-8

from sqlalchemy import Column, String, Integer, create_engine, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from sqlite3 import IntegrityError

DBBase = declarative_base()


def get_db_session(db_file):
    dir_name = os.path.abspath(os.path.dirname(db_file))
    if not os.access(dir_name, os.W_OK):
        raise RuntimeError("{} can not write".format(dir_name))
    connect_url = "sqlite:///{db_file}?check_same_thread=False".format(db_file=db_file)
    engine = create_engine(connect_url)
    DBPlotTasks.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


class DBPlotStop(DBBase):
    __tablename__ = 'plot_stop'
    id = Column(Integer, autoincrement=True, primary_key=True)
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="创建时间")
    worker_id = Column(String(32), comment="本机唯一ID, uuid", nullable=False)
    # task_id = sha256(worker_id#time.time()#fpk#ppk#ksize#cache1#cache2#threads#buffer#dest_type#dest_path)
    task_id = Column(String(64), comment="任务唯一id, hash256", nullable=False, unique=True)
    

class DBPlotTasks(DBBase):
    __tablename__ = 'plot_tasks'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="创建时间")
    worker_id = Column(String(32), comment="本机唯一ID, uuid", nullable=False)
    # task_id = sha256(worker_id#time.time()#fpk#ppk#ksize#cache1#cache2#threads#buffer#dest_type#dest_path)
    task_id = Column(String(64), comment="任务唯一id, hash256", nullable=False, unique=True)
    plot_pid = Column(Integer, comment="P图任务PID", default=0)
    log_pid = Column(Integer, comment="日志收集器PID", default=0)
    status = Column(String(32), comment="当前任务状态", server_default="received")
    plot_id = Column(String(64), comment="当前P图任务ID", default="")
    fpk = Column(String(96), comment="fpk", default="")
    ppk = Column(String(96), comment="ppk", default="")
    memo = Column(String(512), comment="memo", default="")
    ksize = Column(Integer, comment="K SIZE", default=0)
    cache1 = Column(String(1024), comment="cache dir", default="")
    cache2 = Column(String(1024), comment="cache 2 dir", default="")
    threads = Column(Integer, comment="CPU Threads", default=0)
    buffer = Column(Integer, comment="Memory", default=0)
    stripe_size = Column(Integer, comment="stripe size", default=0)
    buckets = Column(Integer, comment="buckets", default=0)
    progress = Column(Float, comment="P图进度", default=0.0)
    
    p1_t1_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t1_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t2_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t2_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t3_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t3_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t4_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t4_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t5_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t5_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t6_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t6_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_t7_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p1_t7_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p1_total_time = Column(Float, comment="p1总耗时", default=0.0)
    p1_total_cpu = Column(Float, comment="p1总耗用cpu", default=0.0)
    p1_table_1_now_size = Column(Integer, comment="table_1_now_size大小", default=0)
    
    p2_t7_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t7_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t7_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t7_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t6_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t6_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t6_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t6_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t5_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t5_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t5_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t5_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t4_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t4_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t4_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t4_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t3_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t3_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t3_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t3_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t2_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t2_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t2_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t2_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_t1_scan_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t1_scan_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p2_t1_sort_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p2_t1_sort_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    
    p2_total_time = Column(Float, comment="p2总耗时", default=0.0)
    p2_total_cpu = Column(Float, comment="p2总耗用cpu", default=0.0)
    
    p3_t1_2_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t1_2_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_t2_3_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t2_3_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_t3_4_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t3_4_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_t4_5_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t4_5_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_t5_6_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t5_6_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_t6_7_time = Column(Float, comment="该阶段花费时间", default=0.0)
    p3_t6_7_cpu = Column(Float, comment="该阶段cpu使用", default=0.0)
    p3_total_time = Column(Float, comment="p3总耗时", default=0.0)
    p3_total_cpu = Column(Float, comment="p3总耗用cpu", default=0.0)
    
    p4_total_time = Column(Float, comment="p4总耗时", default=0.0)
    p4_total_cpu = Column(Float, comment="p4总耗用cpu", default=0.0)
    
    total_time = Column(Float, comment="p1-4总耗时", default=0.0)
    total_cpu = Column(Float, comment="p1-4总耗用cpu", default=0.0)
    copy_time = Column(Float, comment="复制时间", default=0.0)
    copy_cpu = Column(Float, comment="复制耗用cpu", default=0.0)
    dest_type = Column(String(5), comment="最终写入类型", server_default="nfs")
    dest_path = Column(String(1024), comment="最终写入路径", nullable=False)
    dest_file_name = Column(String(1024), comment="最终文件名", default=0.0)
    stage_now = Column(Integer, comment="当前阶段", default=0)
