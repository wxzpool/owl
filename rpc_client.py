#!/usr/bin/env python3
# encoding: utf-8

import grpc
import libs.grpc.talent as pb2_ref
import libs.grpc.talent_pb2 as pb2
import libs.grpc.talent_pb2_grpc as pb2_grpc
import time
import uuid


#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_create")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      # print()
#      # print(stub)
#      # print()
#      req: pb2_ref.PlotTaskCreateRequest = pb2.PlotTaskCreateRequest()
#      # print(req)
#      # print()
#      req.worker_id = "server1"
#      req.task_id = "xyz2"
#      req.plot_config.ppk = "test1"
#      req.plot_config.fpk = "test2"
#      req.plot_config.ksize = 32
#      req.plot_config.threads = 4
#      req.plot_config.buffer = 4000
#      req.plot_config.cache1 = "/cache/level1-1"
#      req.plot_config.cache2 = "/cache/level1-1"
#      req.plot_config.dest.type = "local"
#      req.plot_config.dest.path = "/tmp"
#      resp = stub.plot_task_create(req)
#
#      print("success: %s" % resp.is_success)
#      print(resp)
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_create")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      req = pb2.PlotTaskCreateRequest(task_id="xyz3")
#      resp: pb2_ref.PlotTaskStatusResponse = stub.plot_task_create(req)
#
#      print(resp)
#
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_status")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="xyz3")
#      resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#      print("existed: %s" % resp.existed)
#      print(resp)
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_status")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="xyz")
#      resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#      print("existed: %s" % resp.existed)
#      print("status: %s" % resp.status)
#      print(resp.plot_details)
#
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_status_all")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      resp: pb2_ref.PlotTaskStatusAllResponse = stub.plot_task_status_all(pb2.Empty())
#      for task in resp.tasks:
#          print(task.task_id)
#          print(task.status)
#          print(task.plot_details.id, task.plot_details.progress)
#
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("get_plot_tasks")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(pb2.Empty())
#      for task in resp.tasks:
#          print(task.task_id)
#          print(task.status)
#          print(task.plot_details.id, task.plot_details.progress)
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("plot_task_update")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      req: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
#      req.task_id = "xyz"
#      req.status = "pending"
#      resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(req)
#      print(resp.is_success)
#      print(resp.msg)
task_id = 'task_%s' % uuid.uuid4()

with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("模拟新建了一个任务")
    stub = pb2_grpc.PlotManagerStub(channel)
    req: pb2_ref.PlotTaskCreateRequest = pb2.PlotTaskCreateRequest(task_id=task_id)
    req.plot_config.ksize = 32
    req.plot_config.threads = 2
    req.plot_config.buffer = 3500
    req.plot_config.cache1 = "/cache/level1-1"
    req.plot_config.dest.type = "local"
    req.plot_config.dest.path = "/data/local/disk1"
    req.plot_config.fpk = "fpk"
    req.plot_config.ppk = "ppk"
    req.worker_id = "server1"
    resp: pb2_ref.PlotTaskStatusResponse = stub.plot_task_create(req)
    print("任务创建回执收到, %s" % resp)
    
time.sleep(1)

while True:
    # print("模拟测试")
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        print("获取任务task_id_test_001的状态")
        stub = pb2_grpc.PlotManagerStub(channel)
        req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id=task_id)
        resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
        print("existed: %s" % resp.existed)
        print("status: %s" % resp.status)
        print("received time: %s" % resp.received_time)
        print(resp.plot_details)
    
    time.sleep(1)

# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("获取任务task_id_test_001的状态")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="task_id_test_001")
#     resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#     print("existed: %s" % resp.existed)
#     print("status: %s" % resp.status)
#     print("received time: %s" % resp.received_time)
#     print(resp.plot_details)

# print("模拟主控supervisor排队任务")

# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("首先获取所有状态为received的记录")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(pb2.Empty())
#     for task in resp.tasks:
#         print("task_id: {}, status: {}, plot_id: {}, plot_progress: {}".format(
#             task.task_id,
#             task.status,
#             task.plot_details.id,
#             task.plot_details.progress
#         ))
#
#
# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("排队task_id_test_001")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus(task_id="task_id_test_001")
#     req.status = "pending"
#     req.pending_time = time.time()
#     resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(req)
#     print("is_success: %s" % resp.is_success)
#     print("msg: %s" % resp.msg)
#
#
# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("获取任务task_id_test_001的状态")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="task_id_test_001")
#     resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#     print("existed: %s" % resp.existed)
#     print("status: %s" % resp.status)
#     print("pending time: %s" % resp.pending_time)
#     print(resp.plot_details)
#
#
# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("task_id_test_001 任务开始")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus(task_id="task_id_test_001")
#     req.status = "started"
#     req.started_time = time.time()
#     req.log_pid = 123
#     req.plot_pid = 456
#     resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(req)
#     print("is_success: %s" % resp.is_success)
#     print("msg: %s" % resp.msg)
#
#
# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("获取任务task_id_test_001的状态")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="task_id_test_001")
#     resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#     print("existed: %s" % resp.existed)
#     print("status: %s" % resp.status)
#     print("started time: %s" % resp.started_time)
#     print("logger: %s, plotter: %s" % (resp.log_pid, resp.plot_pid))
#     print(resp.plot_details)
#
# with grpc.insecure_channel('127.0.0.1:50051') as channel:
#     print("task_id_test_001 任务运行")
#     stub = pb2_grpc.PlotManagerStub(channel)
#     req: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus(task_id="task_id_test_001")
#     req.status = "running"
#     req.running_time = time.time()
#     req.plot_details.id = "some id"
#     req.plot_details.memo = "memo xxx"
#     req.plot_details.stage_now = 0
#     req.plot_details.buckets = 128
#     req.plot_details.stripe_size = 65536
#     req.plot_details.progress = 1.0
#     resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(req)
#     print("is_success: %s" % resp.is_success)
#     print("msg: %s" % resp.msg)

#  time.sleep(15)
#
#  with grpc.insecure_channel('127.0.0.1:50051') as channel:
#      print("获取任务task_id_test_001的状态")
#      stub = pb2_grpc.PlotManagerStub(channel)
#      req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="task_id_test_001")
#      resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
#      print("existed: %s" % resp.existed)
#      print("status: %s" % resp.status)
#      print("running time: %s" % resp.running_time)
#      print("logger: %s, plotter: %s" % (resp.log_pid, resp.plot_pid))
#      print(resp.plot_details)
