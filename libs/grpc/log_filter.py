#!/usr/bin/env python3
# encoding: utf-8

import re
# from sys import stdin, stderr, stdout, argv
# import datetime
from os import path
import libs.sturcts as structs


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


class P1Status(structs.PlotP1Status):
    stage = "p1"
    now = 0


class P2Status(structs.PlotP2Status):
    now = 0
    stage = "p2"


class P3Status(structs.PlotP3Status):
    now = None
    stage = "p3"


class P4Status(structs.PlotP4Status):
    stage = "p4"


class LogFilter(structs.PlotDetails):
    is_started: bool = False
    is_finished: bool = False
    
    def parser(self, s: str):
        # print(s)
        if self.is_finished:
            return
        if not self.is_started:
            self._is_started(s)
        if self._get_id(s):
            return
        if self._get_plots_size(s):
            return
        if self._get_cache(s):
            return
        if self._get_buffer(s):
            return
        if self._get_buckets(s):
            return
        if self._get_threads_stripe_size(s):
            return
        if self._which_stage(s):
            return
        if self._process_stage_info(s):
            return
        # if self._get_phase_1_time(s):
        #     return
        # if self._get_phase_2_time(s):
        #     return
        # if self._get_phase_3_time(s):
        #     return
        # if self._get_phase_4_time(s):
        #     return
        if self._get_total_time(s):
            return
        if self._get_copy_time(s):
            return
        if self._is_finished(s):
            return
    
    def _process_stage_info(self, s: str) -> bool:
        if self.stage_now == 0:
            return True
        if self.stage_now == 1:
            if self.phase_1_status is None:
                self.phase_1_status = P1Status()
            if self._which_p1_stage(s):
                return True
            _time, _cpu = self._get_p1_info(s)
            # print("[debug] p1-%s, t: %s c: %s" % (self.phase_1_status.now, _time, _cpu))
            if _time != 0.0 and _cpu != 0.0:
                _p1_now = self.phase_1_status.now
                _target = "t%s" % _p1_now
                if self.phase_1_status.__getattribute__(_target) is None:
                    self.phase_1_status.__setattr__(_target, structs.PlotPhaseStatus())
                self.phase_1_status.__dict__[_target].stage = _target
                self.phase_1_status.__dict__[_target].time = _time
                self.phase_1_status.__dict__[_target].cpu_usage = _cpu
                # setattr(self.phase_1_status, "t%s" % _p1_now, _target)
                # print("[debug] %s" % _target)
                return True
            _time, _cpu = self._get_phase_1_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.phase_1_status.time = _time
                self.phase_1_status.cpu_usage = _cpu
                return True
        if self.stage_now == 2:
            if self.phase_2_status is None:
                self.phase_2_status = P2Status()
            if self._which_p2_stage(s):
                return True
            _time, _cpu = self._get_p2_scan_info(s)
            if _time != 0.0 and _cpu != 0.0:
                _p2_now = self.phase_2_status.now
                _target = "t%s" % _p2_now
                if self.phase_2_status.__getattribute__(_target) is None:
                    self.phase_2_status.__setattr__(_target, structs.PlotP2BaseStatus())
                # print("[debug] %s" % self.phase_2_status.__getattribute__(_target))
                if self.phase_2_status.__dict__[_target].scan is None:
                    self.phase_2_status.__dict__[_target].scan = structs.PlotPhaseStatus()
                self.phase_2_status.__dict__[_target].scan.stage = _target
                self.phase_2_status.__dict__[_target].scan.time = _time
                self.phase_2_status.__dict__[_target].scan.cpu_usage = _cpu
                return True
            _time, _cpu = self._get_p2_sort_info(s)
            if _time != 0.0 and _cpu != 0.0:
                _p2_now = self.phase_2_status.now
                _target = "t%s" % _p2_now
                if self.phase_2_status.__getattribute__(_target) is None:
                    self.phase_2_status.__setattr__(_target, structs.PlotP2BaseStatus())
                # print("[debug] %s" % self.phase_2_status.__getattribute__(_target))
                if self.phase_2_status.__dict__[_target].sort is None:
                    self.phase_2_status.__dict__[_target].sort = structs.PlotPhaseStatus()
                self.phase_2_status.__dict__[_target].sort.stage = _target
                self.phase_2_status.__dict__[_target].sort.time = _time
                self.phase_2_status.__dict__[_target].sort.cpu_usage = _cpu
                return True
            _time, _cpu = self._get_phase_2_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.phase_2_status.time = _time
                self.phase_2_status.cpu_usage = _cpu
                return True
            if self._get_wrote(s):
                return True
        if self.stage_now == 3:
            if self.phase_3_status is None:
                self.phase_3_status = P3Status()
            if self._which_p3_stage(s):
                return True
            _time, _cpu = self._get_p3_scan_info(s)
            # print('[debug] %s %s' % (_time, _cpu))
            if _time != 0.0 and _cpu != 0.0:
                _target = "t%s" % self.phase_3_status.now
                if self.phase_3_status.__getattribute__(_target) is None:
                    self.phase_3_status.__setattr__(_target, structs.PlotPhaseStatus())
                self.phase_3_status.__dict__[_target].stage = _target
                self.phase_3_status.__dict__[_target].time = _time
                self.phase_3_status.__dict__[_target].cpu_usage = _cpu
            _time, _cpu = self._get_phase_3_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.phase_3_status.time = _time
                self.phase_3_status.cpu_usage = _cpu
                return True
        if self.stage_now == 4:
            if self.phase_4_status is None:
                self.phase_4_status = P4Status()
            _time, _cpu = self._get_phase_4_time(s)
            if _time != 0.0 and _cpu != 0.0:
                self.phase_4_status.time = _time
                self.phase_4_status.cpu_usage = _cpu
                return True
        return False
    
    def _which_p3_stage(self, s: str) -> bool:
        # Compressing tables 1 and 2
        reg = re.compile(r'^Compressing\s+tables\s+(?P<b1>\d)\s+and\s+(?P<b2>\d)')
        t = reg.search(s)
        if t is not None and 'b1' in t.groupdict() and 'b2' in t.groupdict():
            self.phase_3_status.now = "%s_%s" % (t.groupdict()['b1'], t.groupdict()['b2'])
            return True
        return False
    
    def _which_p2_stage(self, s: str) -> bool:
        reg = re.compile(r'^Backpropagating\s+on\s+table\s+(?P<stage>\d)')
        t = reg.search(s)
        if t is not None and 'stage' in t.groupdict():
            self.phase_2_status.now = int(t.groupdict()['stage'])
            # print("[debug] p2 = %s" % self.phase_2_status.now)
            return True
        return False
    
    def _which_p1_stage(self, s: str) -> bool:
        reg = re.compile(r'^Computing\s+table\s+(?P<stage>\d)')
        t = reg.search(s)
        if t is not None and 'stage' in t.groupdict():
            self.phase_1_status.now = int(t.groupdict()['stage'])
            # print("[debug] p1 = %s" % self.phase_1_status.now)
            return True
        return False
    
    def _get_wrote(self, s: str) -> bool:
        reg = re.compile(r'^Wrote:\s+(?P<wrote>\d+).*')
        t = reg.search(s)
        if t is not None and 'wrote' in t.groupdict():
            self.wrote = int(t.groupdict()['wrote'])
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
        if self.phase_2_status.now == 7:
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
            self.stage_now = int(t.groupdict()['stage'])
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
            self.pool_key = t.groupdict()['pool_key']
            self.farmer_key = t.groupdict()['farmer_key']
            self.is_started = True
            # print(self)
            self.progress = 1.0
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
            self.file_full_path = t.groupdict()['file_full_path']
            self.file_name = path.basename(self.file_full_path)
            self.is_finished = True
            # print(self)
            return True
        return False
    
    def _get_id(self, s: str) -> bool:
        # ID: 3c99851e3fa6a8f1bc4025ac3a18773ef34a19ae27b792cd9482442dfac75d2e
        reg = re.compile(r'^ID:\s+(?P<id>\w+)')
        t = reg.search(s)
        if t is not None and 'id' in t.groupdict():
            self.id = t.groupdict()['id']
            return True
        return False
    
    def _get_plots_size(self, s: str) -> bool:
        # Plot size is: 32
        reg = re.compile(r'^Plot\s+size\s+is:\s+(?P<plots_size>\d+)')
        t = reg.search(s)
        if t is not None and 'plots_size' in t.groupdict():
            self.plots_size = int(t.groupdict()['plots_size'])
            return True
        return False
    
    def _get_cache(self, s: str) -> bool:
        # Starting plotting progress into temporary dirs: /cache/level1-1 and /cache/level1-1
        reg = re.compile(r'^Starting\s+plotting\s+progress\s+into\s+temporary\s+dirs:\s+(?P<level1>[^\s]+)\s+and\s+(?P<level2>.*)')
        t = reg.search(s)
        if t is not None and 'level1' in t.groupdict() and 'level2' in t.groupdict():
            self.cache1 = t.groupdict()['level1']
            self.cache2 = t.groupdict()['level2']
            return True
        return False
    
    def _get_buffer(self, s: str) -> bool:
        # Buffer size is: 4608MiB
        reg = re.compile(r'^Buffer\s+size\s+is:\s+(?P<buffer>\d+)')
        t = reg.search(s)
        if t is not None and 'buffer' in t.groupdict():
            self.buffer = int(t.groupdict()['buffer'])
            return True
        return False
    
    def _get_buckets(self, s: str) -> bool:
        # Using 128 buckets
        reg = re.compile(r'^Using\s+(?P<buckets>\d+)\s+buckets')
        t = reg.search(s)
        if t is not None and 'buckets' in t.groupdict():
            self.buckets = int(t.groupdict()['buckets'])
            return True
        return False
    
    def _get_threads_stripe_size(self, s: str) -> bool:
        # Using 4 threads of stripe size 65536
        reg = re.compile(r'^Using\s+(?P<threads>\d+)\s+threads\s+of\s+stripe\s+size\s+(?P<stripe_size>\d+)')
        t = reg.search(s)
        if t is not None and 'threads' in t.groupdict() and 'stripe_size' in t.groupdict():
            self.threads = int(t.groupdict()['threads'])
            self.stripe_size = int(t.groupdict()['stripe_size'])
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
            self.total_time = structs.PlotPhaseStatus()
            self.total_time.stage = "total"
            self.total_time.time = float(t.groupdict()['time'])
            self.total_time.cpu_usage = float(t.groupdict()['cpu'])
            return True
        return False
    
    def _get_copy_time(self, s: str) -> bool:
        # Copy time = 6522.441 seconds. CPU (1.040%) Fri May  7 01:40:04 2021
        reg = re.compile(
            r'^Copy\s+time\s+=\s+(?P<time>\d+\.\d+)\s+seconds\.\s+CPU\s+\((?P<cpu>\d+\.\d+)%\)\s+.*')
        t = reg.search(s)
        if t is not None and 'time' in t.groupdict() and 'cpu' in t.groupdict():
            self.total_time = structs.PlotPhaseStatus()
            self.total_time.stage = "copy"
            self.total_time.time = float(t.groupdict()['time'])
            self.total_time.cpu_usage = float(t.groupdict()['cpu'])
            return True
        return False
