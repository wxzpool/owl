# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: talent.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List, Optional

import betterproto
import grpclib


@dataclass
class PlotPhaseStatus(betterproto.Message):
    stage: str = betterproto.string_field(1)
    time: float = betterproto.float_field(2)
    cpu_usage: float = betterproto.float_field(3)


@dataclass
class PlotP2BaseStatus(betterproto.Message):
    stage: str = betterproto.string_field(1)
    scan: "PlotPhaseStatus" = betterproto.message_field(2)
    sort: "PlotPhaseStatus" = betterproto.message_field(3)


@dataclass
class PlotP1Status(betterproto.Message):
    stage: str = betterproto.string_field(1)
    table_1_now_size: int = betterproto.int32_field(2)
    t1: "PlotPhaseStatus" = betterproto.message_field(3)
    t2: "PlotPhaseStatus" = betterproto.message_field(4)
    t3: "PlotPhaseStatus" = betterproto.message_field(5)
    t4: "PlotPhaseStatus" = betterproto.message_field(6)
    t5: "PlotPhaseStatus" = betterproto.message_field(7)
    t6: "PlotPhaseStatus" = betterproto.message_field(8)
    t7: "PlotPhaseStatus" = betterproto.message_field(9)
    now: int = betterproto.int32_field(10)
    time: float = betterproto.float_field(11)
    cpu_usage: float = betterproto.float_field(12)


@dataclass
class PlotP2Status(betterproto.Message):
    stage: str = betterproto.string_field(1)
    t7: "PlotP2BaseStatus" = betterproto.message_field(2)
    t6: "PlotP2BaseStatus" = betterproto.message_field(3)
    t5: "PlotP2BaseStatus" = betterproto.message_field(4)
    t4: "PlotP2BaseStatus" = betterproto.message_field(5)
    t3: "PlotP2BaseStatus" = betterproto.message_field(6)
    t2: "PlotP2BaseStatus" = betterproto.message_field(7)
    t1: "PlotP2BaseStatus" = betterproto.message_field(8)
    now: int = betterproto.int32_field(9)
    time: float = betterproto.float_field(10)
    cpu_usage: float = betterproto.float_field(11)


@dataclass
class PlotP3Status(betterproto.Message):
    stage: str = betterproto.string_field(1)
    t1_2: "PlotPhaseStatus" = betterproto.message_field(2)
    t2_3: "PlotPhaseStatus" = betterproto.message_field(3)
    t3_4: "PlotPhaseStatus" = betterproto.message_field(4)
    t4_5: "PlotPhaseStatus" = betterproto.message_field(5)
    t5_6: "PlotPhaseStatus" = betterproto.message_field(6)
    t6_7: "PlotPhaseStatus" = betterproto.message_field(7)
    now: str = betterproto.string_field(8)
    time: float = betterproto.float_field(9)
    cpu_usage: float = betterproto.float_field(10)


@dataclass
class PlotDetails(betterproto.Message):
    fpk: str = betterproto.string_field(1)
    ppk: str = betterproto.string_field(2)
    id: str = betterproto.string_field(3)
    ksize: int = betterproto.int32_field(4)
    cache1: str = betterproto.string_field(5)
    cache2: str = betterproto.string_field(6)
    buffer: int = betterproto.int32_field(7)
    buckets: int = betterproto.int32_field(8)
    threads: int = betterproto.int32_field(9)
    stripe_size: int = betterproto.int32_field(10)
    phase_1_status: "PlotP1Status" = betterproto.message_field(11)
    phase_2_status: "PlotP2Status" = betterproto.message_field(12)
    phase_3_status: "PlotP3Status" = betterproto.message_field(13)
    phase_4_status: "PlotPhaseStatus" = betterproto.message_field(14)
    total_time: "PlotPhaseStatus" = betterproto.message_field(15)
    copy_time: "PlotPhaseStatus" = betterproto.message_field(16)
    dest_file_name: str = betterproto.string_field(17)
    dest_path: str = betterproto.string_field(18)
    dest_type: str = betterproto.string_field(19)
    wrote: int = betterproto.int32_field(20)
    stage_now: int = betterproto.int32_field(21)
    progress: float = betterproto.float_field(22)
    memo: str = betterproto.string_field(23)


@dataclass
class PlotConfig(betterproto.Message):
    fpk: str = betterproto.string_field(1)
    ppk: str = betterproto.string_field(2)
    ksize: int = betterproto.int32_field(3)
    threads: int = betterproto.int32_field(4)
    buffer: int = betterproto.int32_field(5)
    cache1: str = betterproto.string_field(6)
    cache2: str = betterproto.string_field(7)
    dest: "PlotConfigDest" = betterproto.message_field(8)


@dataclass
class PlotConfigDest(betterproto.Message):
    type: str = betterproto.string_field(1)
    path: str = betterproto.string_field(2)


@dataclass
class PlotTaskCreateRequest(betterproto.Message):
    task_id: str = betterproto.string_field(1)
    worker_id: str = betterproto.string_field(2)
    plot_config: "PlotConfig" = betterproto.message_field(3)


@dataclass
class PlotTaskStatus(betterproto.Message):
    worker_id: str = betterproto.string_field(1)
    task_id: str = betterproto.string_field(2)
    existed: bool = betterproto.bool_field(3)
    plot_pid: int = betterproto.int32_field(4)
    log_pid: int = betterproto.int32_field(5)
    status: str = betterproto.string_field(6)
    plot_details: "PlotDetails" = betterproto.message_field(7)


@dataclass
class PlotTaskStatusAllResponse(betterproto.Message):
    tasks: List["PlotTaskStatus"] = betterproto.message_field(1)


@dataclass
class PlotTaskIdRequest(betterproto.Message):
    task_id: str = betterproto.string_field(1)


@dataclass
class PlotTaskStopRequest(betterproto.Message):
    task_id: str = betterproto.string_field(1)
    reason: str = betterproto.string_field(2)


@dataclass
class GetPlotTaskResponse(betterproto.Message):
    # 所有未执行的任务列表
    task_list: List["PlotConfig"] = betterproto.message_field(1)


@dataclass
class PlotTaskStatusResponse(betterproto.Message):
    type: str = betterproto.string_field(1)
    is_success: bool = betterproto.bool_field(2)
    msg: str = betterproto.string_field(3)


@dataclass
class PlotTaskUpdateResponse(betterproto.Message):
    is_success: bool = betterproto.bool_field(1)
    msg: str = betterproto.string_field(2)


@dataclass
class Empty(betterproto.Message):
    pass


class PlotManagerStub(betterproto.ServiceStub):
    async def plot_task_create(
        self,
        *,
        task_id: str = "",
        worker_id: str = "",
        plot_config: Optional["PlotConfig"] = None,
    ) -> PlotTaskStatusResponse:
        request = PlotTaskCreateRequest()
        request.task_id = task_id
        request.worker_id = worker_id
        if plot_config is not None:
            request.plot_config = plot_config

        return await self._unary_unary(
            "/talent.PlotManager/plot_task_create",
            request,
            PlotTaskStatusResponse,
        )

    async def plot_task_status(self, *, task_id: str = "") -> PlotTaskStatus:
        request = PlotTaskIdRequest()
        request.task_id = task_id

        return await self._unary_unary(
            "/talent.PlotManager/plot_task_status",
            request,
            PlotTaskStatus,
        )

    async def plot_task_status_all(self) -> PlotTaskStatusAllResponse:
        request = Empty()

        return await self._unary_unary(
            "/talent.PlotManager/plot_task_status_all",
            request,
            PlotTaskStatusAllResponse,
        )

    async def plot_task_stop(
        self, *, task_id: str = "", reason: str = ""
    ) -> PlotTaskStatusResponse:
        request = PlotTaskStopRequest()
        request.task_id = task_id
        request.reason = reason

        return await self._unary_unary(
            "/talent.PlotManager/plot_task_stop",
            request,
            PlotTaskStatusResponse,
        )

    async def plot_task_update(
        self,
        *,
        worker_id: str = "",
        task_id: str = "",
        existed: bool = False,
        plot_pid: int = 0,
        log_pid: int = 0,
        status: str = "",
        plot_details: Optional["PlotDetails"] = None,
    ) -> PlotTaskUpdateResponse:
        request = PlotTaskStatus()
        request.worker_id = worker_id
        request.task_id = task_id
        request.existed = existed
        request.plot_pid = plot_pid
        request.log_pid = log_pid
        request.status = status
        if plot_details is not None:
            request.plot_details = plot_details

        return await self._unary_unary(
            "/talent.PlotManager/plot_task_update",
            request,
            PlotTaskUpdateResponse,
        )

    async def get_plot_tasks(self) -> PlotTaskStatusAllResponse:
        request = Empty()

        return await self._unary_unary(
            "/talent.PlotManager/get_plot_tasks",
            request,
            PlotTaskStatusAllResponse,
        )
