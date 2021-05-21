#!/usr/bin/env python3
# encoding: utf-8

class PlotPhaseStatus(object):
    stage: str
    time: float
    cpu_usage: float


class PlotP2BaseStatus(object):
    stage: str
    scan: PlotPhaseStatus = None
    sort: PlotPhaseStatus = None


class PlotP1Status(PlotPhaseStatus):
    now = 0
    stage = "p1"
    table_1_now_size: int
    t1: PlotPhaseStatus = None
    t2: PlotPhaseStatus = None
    t3: PlotPhaseStatus = None
    t4: PlotPhaseStatus = None
    t5: PlotPhaseStatus = None
    t6: PlotPhaseStatus = None
    t7: PlotPhaseStatus = None


class PlotP2Status(PlotPhaseStatus):
    now = 0
    stage = "p2"
    t7: PlotP2BaseStatus = None
    t6: PlotP2BaseStatus = None
    t5: PlotP2BaseStatus = None
    t4: PlotP2BaseStatus = None
    t3: PlotP2BaseStatus = None
    t2: PlotP2BaseStatus = None
    t1: PlotP2BaseStatus = None


class PlotP3Status(PlotPhaseStatus):
    now = None
    stage = "p3"
    t1_2: PlotPhaseStatus = None
    t2_3: PlotPhaseStatus = None
    t3_4: PlotPhaseStatus = None
    t4_5: PlotPhaseStatus = None
    t5_6: PlotPhaseStatus = None
    t6_7: PlotPhaseStatus = None


class PlotP4Status(PlotPhaseStatus):
    stage = "p4"


class PlotDetails(object):
    pool_key: str = None
    farmer_key: str = None
    id: str = None
    plots_size: int = None
    cache1: str = None
    cache2: str = None
    buffer: int = None
    buckets: int = None
    threads: int = None
    stripe_size: int = None
    phase_1_status: PlotP1Status = None
    phase_2_status: PlotP2Status = None
    phase_3_status: PlotP3Status = None
    phase_4_status: PlotP4Status = None
    total_time: PlotPhaseStatus = None
    copy_time: PlotPhaseStatus = None
    file_name: str = None
    file_full_path: str = None
    wrote: int = 0
    is_started: bool = False
    is_finished: bool = False
    _stage_now: int = 0
    _progress: float = 0.0
