#!/usr/bin/env python3
# encoding: utf-8

import grpc
import libs.grpc.talent as pb2_ref
import libs.grpc.talent_pb2 as pb2
import libs.grpc.talent_pb2_grpc as pb2_grpc


with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_create")
    stub = pb2_grpc.PlotManagerStub(channel)
    # print()
    # print(stub)
    # print()
    req: pb2_ref.PlotTaskCreateRequest = pb2.PlotTaskCreateRequest()
    # print(req)
    # print()
    req.worker_id = "server1"
    req.task_id = "xyz2"
    req.plot_config.ppk = "test1"
    req.plot_config.fpk = "test2"
    req.plot_config.ksize = 32
    req.plot_config.threads = 4
    req.plot_config.buffer = 4000
    req.plot_config.cache1 = "/cache/level1-1"
    req.plot_config.cache2 = "/cache/level1-1"
    req.plot_config.dest.type = "local"
    req.plot_config.dest.path = "/tmp"
    resp = stub.plot_task_create(req)

    print("success: %s" % resp.is_success)
    print(resp)

with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_create")
    stub = pb2_grpc.PlotManagerStub(channel)
    req = pb2.PlotTaskCreateRequest(task_id="xyz3")
    resp: pb2_ref.PlotTaskStatusResponse = stub.plot_task_create(req)
    
    print(resp)


with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_status")
    stub = pb2_grpc.PlotManagerStub(channel)
    req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="xyz3")
    resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
    print("existed: %s" % resp.existed)
    print(resp)

with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_status")
    stub = pb2_grpc.PlotManagerStub(channel)
    req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest(task_id="xyz")
    resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)
    print("existed: %s" % resp.existed)
    print("status: %s" % resp.status)
    print(resp.plot_details)


with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_status_all")
    stub = pb2_grpc.PlotManagerStub(channel)
    resp: pb2_ref.PlotTaskStatusAllResponse = stub.plot_task_status_all(pb2.Empty())
    for task in resp.tasks:
        print(task.task_id)
        print(task.status)
        print(task.plot_details.id, task.plot_details.progress)


with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("get_plot_tasks")
    stub = pb2_grpc.PlotManagerStub(channel)
    resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(pb2.Empty())
    for task in resp.tasks:
        print(task.task_id)
        print(task.status)
        print(task.plot_details.id, task.plot_details.progress)

with grpc.insecure_channel('127.0.0.1:50051') as channel:
    print("plot_task_update")
    stub = pb2_grpc.PlotManagerStub(channel)
    req: pb2_ref.PlotTaskStatus = pb2.PlotTaskStatus()
    req.task_id = "xyz"
    req.status = "pending"
    resp: pb2_ref.PlotTaskUpdateResponse = stub.plot_task_update(req)
    print(resp.is_success)
    print(resp.msg)
