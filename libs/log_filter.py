#!/usr/bin/env python3
# encoding: utf-8

import re
# from sys import stdin, stderr, stdout, argv
# import datetime
from os import path
from .grpc import talent as pb2_ref
# import time


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


class LogFilter(object):
    store: pb2_ref.PlotTaskStatus
    
    def get_status(self):
        return self.store
    
    def __init__(self, store):
        self.store = store
        # self.store.phase_1_status = pb2.PlotP1Status()
        self.store.plot_details.phase_1_status.stage = "p1"
        # self.store.phase_1_status.t1 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t2 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t3 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t4 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t5 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t6 = pb2.PlotPhaseStatus()
        # self.store.phase_1_status.t7 = pb2.PlotPhaseStatus()
        
        # self.store.phase_2_status = pb2.PlotP2Status()
        self.store.plot_details.phase_2_status.stage = "p2"
        # self.store.phase_2_status.t7.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t7.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t6.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t6.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t5.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t5.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t4.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t4.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t3.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t3.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t2.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t2.sort = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t1.scan = pb2.PlotP2BaseStatus()
        # self.store.phase_2_status.t1.sort = pb2.PlotP2BaseStatus()
        
        # self.store.phase_3_status = pb2.PlotP3Status()
        self.store.plot_details.phase_3_status.stage = "p3"
        # self.store.phase_3_status.t1_2 = pb2.PlotPhaseStatus()
        # self.store.phase_3_status.t2_3 = pb2.PlotPhaseStatus()
        # self.store.phase_3_status.t3_4 = pb2.PlotPhaseStatus()
        # self.store.phase_3_status.t4_5 = pb2.PlotPhaseStatus()
        # self.store.phase_3_status.t5_6 = pb2.PlotPhaseStatus()
        # self.store.phase_3_status.t6_7 = pb2.PlotPhaseStatus()
        
        # self.store.phase_4_status = pb2.PlotPhaseStatus()
        self.store.plot_details.phase_4_status.stage = "p4"

    def parser(self, s: str) -> bool:
        # print(s)
        if self.store.plot_details.is_finished:
            return True
        if not self.store.plot_details.is_started:
            if self._is_started(s):
                return True
        if self._get_memo(s):
            return True
        if self._get_id(s):
            return True
        if self._get_plots_size(s):
            return True
        if self._get_cache(s):
            return True
        if self._get_buffer(s):
            return True
        if self._get_buckets(s):
            return True
        if self._get_threads_stripe_size(s):
            return True
        if self._which_stage(s):
            return True
        if self._process_stage_info(s):
            return True
        if self._get_total_time(s):
            return True
        if self._get_copy_time(s):
            return True
        if self._is_finished(s):
            return True
        return False
    
    def _p1_details_writer(self, now, _time, _cpu):
        _base = 10.0
        if now == 1:
            self.store.plot_details.phase_1_status.t1.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t1.time = _time
            self.store.plot_details.phase_1_status.t1.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 2:
            self.store.plot_details.phase_1_status.t2.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t2.time = _time
            self.store.plot_details.phase_1_status.t2.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 3:
            self.store.plot_details.phase_1_status.t3.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t3.time = _time
            self.store.plot_details.phase_1_status.t3.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 4:
            self.store.plot_details.phase_1_status.t4.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t4.time = _time
            self.store.plot_details.phase_1_status.t4.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 5:
            self.store.plot_details.phase_1_status.t5.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t5.time = _time
            self.store.plot_details.phase_1_status.t5.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 6:
            self.store.plot_details.phase_1_status.t6.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t6.time = _time
            self.store.plot_details.phase_1_status.t6.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
        if now == 7:
            self.store.plot_details.phase_1_status.t7.stage = "t%s" % now
            self.store.plot_details.phase_1_status.t7.time = _time
            self.store.plot_details.phase_1_status.t7.cpu_usage = _cpu
            self.store.plot_details.progress = _base + now * 4
    
    def _p2_details_scan_writer(self, now, _time, _cpu):
        if now == 7:
            self.store.plot_details.phase_2_status.t7.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t7.scan.time = _time
            self.store.plot_details.phase_2_status.t7.scan.cpu_usage = _cpu
            # p2 7 没有sort
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + 40
        if now == 6:
            self.store.plot_details.phase_2_status.t6.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t6.scan.time = _time
            self.store.plot_details.phase_2_status.t6.scan.cpu_usage = _cpu
        if now == 5:
            self.store.plot_details.phase_2_status.t5.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t5.scan.time = _time
            self.store.plot_details.phase_2_status.t5.scan.cpu_usage = _cpu
        if now == 4:
            self.store.plot_details.phase_2_status.t4.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t4.scan.time = _time
            self.store.plot_details.phase_2_status.t4.scan.cpu_usage = _cpu
        if now == 3:
            self.store.plot_details.phase_2_status.t3.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t3.scan.time = _time
            self.store.plot_details.phase_2_status.t3.scan.cpu_usage = _cpu
        if now == 2:
            self.store.plot_details.phase_2_status.t2.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t2.scan.time = _time
            self.store.plot_details.phase_2_status.t2.scan.cpu_usage = _cpu
        if now == 1:
            self.store.plot_details.phase_2_status.t1.scan.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t1.scan.time = _time
            self.store.plot_details.phase_2_status.t1.scan.cpu_usage = _cpu
        
    def _p2_details_sort_writer(self, now, _time, _cpu):
        _base = 40.0
        # self.store.progress = (abs(self.store.phase_2_status.now - 7) + 1) * 3.0 + 40
        if now == 7:
            self.store.plot_details.phase_2_status.t7.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t7.sort.time = _time
            self.store.plot_details.phase_2_status.t7.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 6:
            self.store.plot_details.phase_2_status.t6.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t6.sort.time = _time
            self.store.plot_details.phase_2_status.t6.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 5:
            self.store.plot_details.phase_2_status.t5.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t5.sort.time = _time
            self.store.plot_details.phase_2_status.t5.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 4:
            self.store.plot_details.phase_2_status.t4.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t4.sort.time = _time
            self.store.plot_details.phase_2_status.t4.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 3:
            self.store.plot_details.phase_2_status.t3.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t3.sort.time = _time
            self.store.plot_details.phase_2_status.t3.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 2:
            self.store.plot_details.phase_2_status.t2.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t2.sort.time = _time
            self.store.plot_details.phase_2_status.t2.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base
        if now == 1:
            self.store.plot_details.phase_2_status.t1.sort.stage = "t%s" % now
            self.store.plot_details.phase_2_status.t1.sort.time = _time
            self.store.plot_details.phase_2_status.t1.sort.cpu_usage = _cpu
            self.store.plot_details.progress = (abs(now - 7) + 1) * 3.0 + _base

    def _p3_details_writer(self, now, _time, _cpu):
        _base = 60
        # self.store.progress = float(b1) * 5.0 + 60
        if now == "1_2":
            self.store.plot_details.phase_3_status.t1_2.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t1_2.time = _time
            self.store.plot_details.phase_3_status.t1_2.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
        if now == "2_3":
            self.store.plot_details.phase_3_status.t2_3.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t2_3.time = _time
            self.store.plot_details.phase_3_status.t2_3.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
        if now == "3_4":
            self.store.plot_details.phase_3_status.t3_4.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t3_4.time = _time
            self.store.plot_details.phase_3_status.t3_4.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
        if now == "4_5":
            self.store.plot_details.phase_3_status.t4_5.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t4_5.time = _time
            self.store.plot_details.phase_3_status.t4_5.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
        if now == "5_6":
            self.store.plot_details.phase_3_status.t5_6.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t5_6.time = _time
            self.store.plot_details.phase_3_status.t5_6.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
        if now == "6_7":
            self.store.plot_details.phase_3_status.t6_7.stage = "t%s" % now
            self.store.plot_details.phase_3_status.t6_7.time = _time
            self.store.plot_details.phase_3_status.t6_7.cpu_usage = _cpu
            b1 = float(now[0])
            self.store.plot_details.progress = b1 * 5.0 + _base
    
    def _process_stage_info(self, s: str) -> bool:
        if self.store.plot_details.stage_now == 0:
            self.store.plot_details.progress = 1.0
            return True
        if self.store.plot_details.stage_now == 1:
            # self.store.progress = 10.0
            if self._which_p1_stage(s):
                return True
            _time, _cpu = self._get_p1_info(s)
            # print("[debug] p1-%s, t: %s c: %s" % (self.phase_1_status.now, _time, _cpu))
            if _time != 0.0 and _cpu != 0.0:
                self._p1_details_writer(self.store.plot_details.phase_1_status.now, _time, _cpu)
                return True
            _time, _cpu = self._get_phase_1_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.store.plot_details.phase_1_status.time = _time
                self.store.plot_details.phase_1_status.cpu_usage = _cpu
                return True
        if self.store.plot_details.stage_now == 2:
            # self.store.progress = 40.00
            if self._which_p2_stage(s):
                return True
            _time, _cpu = self._get_p2_scan_info(s)
            if _time != 0.0 and _cpu != 0.0:
                self._p2_details_scan_writer(self.store.plot_details.phase_2_status.now, _time, _cpu)
                return True
            _time, _cpu = self._get_p2_sort_info(s)
            if _time != 0.0 and _cpu != 0.0:
                self._p2_details_sort_writer(self.store.plot_details.phase_2_status.now, _time, _cpu)
                return True
            _time, _cpu = self._get_phase_2_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.store.plot_details.phase_2_status.time = _time
                self.store.plot_details.phase_2_status.cpu_usage = _cpu
                return True
            if self._get_wrote(s):
                return True
        if self.store.plot_details.stage_now == 3:
            # self.store.progress = 60.00
            if self._which_p3_stage(s):
                return True
            _time, _cpu = self._get_p3_scan_info(s)
            # print('[debug] %s %s' % (_time, _cpu))
            if _time != 0.0 and _cpu != 0.0:
                self._p3_details_writer(self.store.plot_details.phase_3_status.now, _time, _cpu)
            _time, _cpu = self._get_phase_3_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.store.plot_details.phase_3_status.time = _time
                self.store.plot_details.phase_3_status.cpu_usage = _cpu
                return True
        if self.store.plot_details.stage_now == 4:
            self.store.plot_details.progress = 90.00
            _time, _cpu = self._get_phase_4_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.store.plot_details.phase_4_status.time = _time
                self.store.plot_details.phase_4_status.cpu_usage = _cpu
                self.store.plot_details.progress = 95.0
                return True
        return False
    
    def _which_p3_stage(self, s: str) -> bool:
        # Compressing tables 1 and 2
        reg = re.compile(r'^Compressing\s+tables\s+(?P<b1>\d)\s+and\s+(?P<b2>\d)')
        t = reg.search(s)
        if t is not None and 'b1' in t.groupdict() and 'b2' in t.groupdict():
            b1 = t.groupdict()['b1']
            self.store.plot_details.phase_3_status.now = "%s_%s" % (b1, t.groupdict()['b2'])
            # self.store.progress = float(b1) * 5.0 + 60
            return True
        return False
    
    def _which_p2_stage(self, s: str) -> bool:
        reg = re.compile(r'^Backpropagating\s+on\s+table\s+(?P<stage>\d)')
        t = reg.search(s)
        if t is not None and 'stage' in t.groupdict():
            self.store.plot_details.phase_2_status.now = int(t.groupdict()['stage'])
            # self.store.progress = (abs(self.store.phase_2_status.now - 7) + 1) * 3.0 + 40
            # print("[debug] p2 = %s" % self.phase_2_status.now)
            return True
        return False
    
    def _which_p1_stage(self, s: str) -> bool:
        reg = re.compile(r'^Computing\s+table\s+(?P<stage>\d)')
        t = reg.search(s)
        if t is not None and 'stage' in t.groupdict():
            self.store.plot_details.phase_1_status.now = int(t.groupdict()['stage'])
            # self.store.progress = self.store.phase_1_status.now * 4.0 + 10
            # print(self.store.progress)
            # print("[debug] p1 = %s" % self.phase_1_status.now)
            return True
        return False
    
    def _get_wrote(self, s: str) -> bool:
        reg = re.compile(r'^Wrote:\s+(?P<wrote>\d+).*')
        t = reg.search(s)
        if t is not None and 'wrote' in t.groupdict():
            self.store.plot_details.wrote = int(t.groupdict()['wrote'])
            return True
        return False
    
    @staticmethod
    def _get_p3_scan_info(s: str) -> (float, float):
        # Total compress table time: 3983.308 seconds. CPU (85.860%) Mon May 17 04:26:15 2021
        reg = re.compile(r'^Total\s+compress\s+table\s+time:\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            return float(t.groupdict()['time']), float(t.groupdict()['cpu'])
        return 0.0, 0.0
    
    @staticmethod
    def _get_p2_scan_info(s: str) -> (float, float):
        # scanned time =  236.135 seconds. CPU (60.780%) Sun May 16 23:48:14 2021
        reg = re.compile(r'^scanned\s+time\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            return float(t.groupdict()['time']), float(t.groupdict()['cpu'])
        return 0.0, 0.0
    
    def _get_p2_sort_info(self, s: str) -> (float, float):
        # sort time =  1842.634 seconds. CPU (95.480%) Mon May 17 00:39:26 2021
        if self.store.plot_details.phase_2_status.now == 7:
            return 0.0, 0.0
        reg = re.compile(r'^sort\s+time\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            return float(t.groupdict()['time']), float(t.groupdict()['cpu'])
        return 0.0, 0.0
    
    @staticmethod
    def _get_p1_info(s: str) -> (float, float):
        time = 0.0
        cpu = 0.0
        reg = re.compile(r'^F1\s+complete,\s+time:\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            return float(t.groupdict()['time']), float(t.groupdict()['cpu'])
        reg = re.compile(r'^Forward\s+propagation\s+table\s+time:\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            return float(t.groupdict()['time']), float(t.groupdict()['cpu'])
        return time, cpu
    
    def _which_stage(self, s: str) -> bool:
        reg = re.compile(r'^Starting phase (?P<stage>\d)/4: .*')
        t = reg.search(s)
        if t is not None and 'stage' in t.groupdict():
            self.store.plot_details.stage_now = int(t.groupdict()['stage'])
            return True
        return False
    
    def _is_started(self, s: str) -> bool:
        # 2021-05-08T17:09:48.988  chia.plotting.create_plots       : ^[[32mINFO    ^[[0m Creating 1 plots of size 32, pool public key:  a0e82a32854d3ab3714ec487c79f88d2b2b109ad981ccb5bc9790d5f3a82105ae82f3325307460eb62c174f507b81782 farmer public key: 98b0a05b016fb261a6dae9dd5a0cd305530deb4cf379a505813d5e5f34001c58d1b8461b161d313fb92f4f0a02a9366d^[[0m
        reg = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\s+chia\.plotting\.create_plots\s+:\s+INFO\s+\s+Creating 1 plots of size 32, pool public key:\s+(?P<pool_key>[^\s]+)\s+farmer public key:\s+(?P<farmer_key>\w+)')
        # print(s)
        t = reg.search(s)
        # print(t)
        # if t:
        #     print(t.groupdict())
        if t is not None and 'pool_key' in t.groupdict() and 'farmer_key' in t.groupdict():
            # print('start')
            self.store.plot_details.ppk = t.groupdict()['pool_key']
            self.store.plot_details.fpk = t.groupdict()['farmer_key']
            self.store.plot_details.is_started = True
            # print(self)
            self.store.status = "running"
            self.store.plot_details.progress = 1.0
            return True
        return False
    
    def _is_finished(self, s: str) -> bool:
        # 2021-05-09T01:55:50.569  chia.plotting.create_plots       : ^[[32mINFO    ^[[0m plot-k32-2021-05-08-17-09-71a382a1b0fb3c4190429eb4d294acc5765ac56909c3736a1a538226562f4c99.plot^[[0m
        # reg = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\s+chia\.plotting\.create_plots\s+:\s+INFO\s+\s+(?P<file_name>plot-k.*\.plot)')
        # Renamed final file from "/data/part3/plot-k33-2021-05-14-15-03-9c67a561fe3250d83d8cdd59975af80b1d1567bb34eced29073b987f378ae781.plot.2.tmp" to "/data/part3/plot-k33-2021-05-14-15-03-9c67a561fe3250d83d8cdd59975af80b1d1567bb34eced29073b987f378ae781.plot"
        reg = re.compile(r'^Renamed\s+final\s+file\s+from\s+"[^"]+"\s+to\s+"(?P<file_full_path>[^"]+)"')
        # print(s)
        t = reg.search(s)
        # if t:
        #     print(t.groupdict())
        # print(t)
        if t is not None and 'file_full_path' in t.groupdict():
            # print('is end')
            self.store.plot_details.dest_path = t.groupdict()['file_full_path']
            self.store.plot_details.dest_file_name = path.basename(self.store.plot_details.dest_path)
            self.store.plot_details.progress = 100
            self.store.plot_details.is_finished = True
            self.store.status = "finished"
            # print(self)
            return True
        return False
    
    def _get_memo(self, s: str) -> bool:
        # 2021-05-16T16:06:03.323  chia.plotting.create_plots       : [32mINFO    [0m Memo: 89b8992f6d30fb87e479fbd8bb7c1c3eba86484d50427ba9b91e6c50d12a5f76de307ffce450b222273c97138395d53797239fc2ed439dbd404724f10505c3f5a4ddfb705591f76720c2d84d172a178d6ed10617afa562a73a657163b2955213326db6f2b57560b2f9ac4f917e909d4ac181e90e4bbfe2f85e5081425ccdf641[0m
        reg = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\s+chia\.plotting\.create_plots\s+:\s+INFO\s+Memo:\s+(?P<memo>\w+)')
        t = reg.search(s)
        if t is not None and 'memo' in t.groupdict():
            self.store.plot_details.memo = t.groupdict()['memo']
            return True
        return False

    def _get_id(self, s: str) -> bool:
        # ID: 3c99851e3fa6a8f1bc4025ac3a18773ef34a19ae27b792cd9482442dfac75d2e
        reg = re.compile(r'^ID:\s+(?P<id>\w+)')
        t = reg.search(s)
        if t is not None and 'id' in t.groupdict():
            self.store.plot_details.id = t.groupdict()['id']
            return True
        return False
    
    def _get_plots_size(self, s: str) -> bool:
        # Plot size is: 32
        reg = re.compile(r'^Plot\s+size\s+is:\s+(?P<plots_size>\d+)')
        t = reg.search(s)
        if t is not None and 'plots_size' in t.groupdict():
            self.store.plot_details.ksize = int(t.groupdict()['plots_size'])
            return True
        return False
    
    def _get_cache(self, s: str) -> bool:
        # Starting plotting progress into temporary dirs: /cache/level1-1 and /cache/level1-1
        reg = re.compile(r'^Starting\s+plotting\s+progress\s+into\s+temporary\s+dirs:\s+(?P<level1>[^\s]+)\s+and\s+(?P<level2>.*)')
        t = reg.search(s)
        if t is not None and 'level1' in t.groupdict() and 'level2' in t.groupdict():
            self.store.plot_details.cache1 = t.groupdict()['level1']
            self.store.plot_details.cache2 = t.groupdict()['level2']
            return True
        return False
    
    def _get_buffer(self, s: str) -> bool:
        # Buffer size is: 4608MiB
        reg = re.compile(r'^Buffer\s+size\s+is:\s+(?P<buffer>\d+)')
        t = reg.search(s)
        if t is not None and 'buffer' in t.groupdict():
            self.store.plot_details.buffer = int(t.groupdict()['buffer'])
            return True
        return False
    
    def _get_buckets(self, s: str) -> bool:
        # Using 128 buckets
        reg = re.compile(r'^Using\s+(?P<buckets>\d+)\s+buckets')
        t = reg.search(s)
        if t is not None and 'buckets' in t.groupdict():
            self.store.plot_details.buckets = int(t.groupdict()['buckets'])
            return True
        return False
    
    def _get_threads_stripe_size(self, s: str) -> bool:
        # Using 4 threads of stripe size 65536
        reg = re.compile(r'^Using\s+(?P<threads>\d+)\s+threads\s+of\s+stripe\s+size\s+(?P<stripe_size>\d+)')
        t = reg.search(s)
        if t is not None and 'threads' in t.groupdict() and 'stripe_size' in t.groupdict():
            self.store.plot_details.threads = int(t.groupdict()['threads'])
            self.store.plot_details.stripe_size = int(t.groupdict()['stripe_size'])
            return True
        return False
    
    @staticmethod
    def _get_phase_1_time(s: str) -> (float, float):
        # Time for phase 1 = 10196.628 seconds. CPU (161.370%) Thu May  6 20:04:42 2021
        reg = re.compile(r'^Time\s+for\s+phase\s+1\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        time = 0.0
        cpu_usage = 0.0
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # print("p1")
            time = float(t.groupdict()['time'])
            cpu_usage = float(t.groupdict()['cpu'])
        return time, cpu_usage
    
    @staticmethod
    def _get_phase_2_time(s: str) -> (float, float):
        reg = re.compile(
            r'^Time\s+for\s+phase\s+2\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        time = 0.0
        cpu_usage = 0.0
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # print("p1")
            time = float(t.groupdict()['time'])
            cpu_usage = float(t.groupdict()['cpu'])
        return time, cpu_usage
    
    @staticmethod
    def _get_phase_3_time(s: str) -> (float, float):
        reg = re.compile(
            r'^Time\s+for\s+phase\s+3\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        time = 0.0
        cpu_usage = 0.0
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # print("p1")
            time = float(t.groupdict()['time'])
            cpu_usage = float(t.groupdict()['cpu'])
        return time, cpu_usage
    
    @staticmethod
    def _get_phase_4_time(s: str) -> (float, float):
        reg = re.compile(
            r'^Time\s+for\s+phase\s+4\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        time = 0.0
        cpu_usage = 0.0
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # print("p1")
            time = float(t.groupdict()['time'])
            cpu_usage = float(t.groupdict()['cpu'])
        return time, cpu_usage
    
    def _get_total_time(self, s: str) -> bool:
        # Total time = 23795.362 seconds. CPU (119.130%) Thu May  6 23:51:20 2021
        reg = re.compile(
            r'^Total\s+time\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # self.store.total_time = pb2.PlotPhaseStatus()
            self.store.plot_details.total_time.stage = "total"
            self.store.plot_details.total_time.time = float(t.groupdict()['time'])
            self.store.plot_details.total_time.cpu_usage = float(t.groupdict()['cpu'])
            return True
        return False
    
    def _get_copy_time(self, s: str) -> bool:
        # Copy time = 6522.441 seconds. CPU (1.040%) Fri May  7 01:40:04 2021
        reg = re.compile(
            r'^Copy\s+time\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            # self.store.total_time = pb2.PlotPhaseStatus()
            self.store.plot_details.copy_time.stage = "copy"
            self.store.plot_details.copy_time.time = float(t.groupdict()['time'])
            self.store.plot_details.copy_time.cpu_usage = float(t.groupdict()['cpu'])
            return True
        return False
