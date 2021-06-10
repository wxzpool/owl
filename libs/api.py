#!/usr/bin/env python
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION: 给Java调用的Restful API 本身就是grpc客户端
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================

import grpc
import libs.grpc.talent as pb2_ref
import libs.grpc.talent_pb2 as pb2
import libs.grpc.talent_pb2_grpc as pb2_grpc
from flask import Flask, request, jsonify, redirect, Response


grpc_host_default = '127.0.0.1:50051'
worker_id_default = 'default'


def create_app(name='owl_api'):
    return Flask(name)


app = create_app('owl_api')


@app.route('/')
def index():
    return jsonify({
        "message": "Owl Api"
    })


@app.route('/plot/task/create', methods=['POST'])
def plot_task_create():
    worker_id = app.config.get('worker_id')
    if worker_id is None:
        worker_id = worker_id_default
    grpc_host = app.config.get('grpc_host')
    if grpc_host is None:
        grpc_host = grpc_host_default
    task_id = request.args.get('task_id')
    if task_id is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('task_id')
        }), 400

    ppk = request.args.get('ppk')
    if ppk is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('ppk')
        }), 400

    fpk = request.args.get('fpk')
    if fpk is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('fpk')
        }), 400

    ksize = request.args.get('ksize')
    if ksize is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('ksize')
        }), 400

    threads = request.args.get('threads')
    if threads is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('threads')
        }), 400

    buffer = request.args.get('buffer')
    if buffer is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('buffer')
        }), 400

    cache1 = request.args.get('cache1')
    if cache1 is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('cache1')
        }), 400

    cache2 = request.args.get('cache2')
    if cache2 is None:
        cache2 = cache1

    dest_type = request.args.get('dest_type')
    if dest_type is None or dest_type not in ['local', 'nfs']:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义或者定义错误，只允许{}".format('dest_type', ['local', 'nfs'])
        }), 400

    dest_path = request.args.get('dest_path')
    if dest_path is None:
        return jsonify({
            "code": 400,
            "message": "参数错误，{}未定义".format('dest_path')
        }), 400

    req: pb2_ref.PlotTaskCreateRequest = pb2.PlotTaskCreateRequest()
    req.worker_id = worker_id

    req.task_id = task_id
    req.plot_config.ppk = ppk
    req.plot_config.fpk = fpk
    req.plot_config.ksize = ksize
    req.plot_config.threads = threads
    req.plot_config.buffer = buffer
    req.plot_config.cache1 = cache1
    req.plot_config.cache2 = cache2
    req.plot_config.dest.type = dest_type
    req.plot_config.dest.path = dest_path

    with grpc.insecure_channel(grpc_host) as channel:
        stub = pb2_grpc.PlotManagerStub(channel)
        resp: pb2_ref.PlotTaskStatusResponse = stub.plot_task_create(req)

    return jsonify({
        "grpc_call": "plot_task_create",
        "args": req.to_dict(),
        "resp": resp.to_dict()
    })


@app.route('/plot/task/status/<task_id>')
def plot_task_status(task_id):
    if task_id is None:
        task_status = request.args.get("status")
        if task_status is None:
            task_status = "running"
        return plot_task_status_all(task_status)
    req: pb2_ref.PlotTaskIdRequest = pb2.PlotTaskIdRequest()
    req.task_id = task_id
    grpc_host = app.config.get('grpc_host')
    if grpc_host is None:
        grpc_host = grpc_host_default

    with grpc.insecure_channel(grpc_host) as channel:
        stub = pb2_grpc.PlotManagerStub(channel)
        resp: pb2_ref.PlotTaskStatus = stub.plot_task_status(req)

    return jsonify({
        "grpc_call": "plot_task_status",
        "args": req.to_dict(),
        "resp": resp.to_dict()
    })


def plot_task_status_all(task_status):
    req: pb2_ref.PlotStatus = pb2.PlotStatus()
    req.status = task_status

    grpc_host = app.config.get('grpc_host')
    if grpc_host is None:
        grpc_host = grpc_host_default

    with grpc.insecure_channel(grpc_host) as channel:
        stub = pb2_grpc.PlotManagerStub(channel)
        resp: pb2_ref.PlotTaskStatusAllResponse = stub.get_plot_tasks(req)

    return jsonify({
        "grpc_call": "get_plot_tasks",
        "args": req.to_dict(),
        "resp": resp.to_dict()
    })




