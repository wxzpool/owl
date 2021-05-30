#!/usr/bin/env python3
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
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

from libs.common import load_cfg, daemonize
from libs.supervisor import Supervisor, PlotProcessCFG, SupervisorCFG, CacheCFG
from libs.talent import Talent, TalentCFG
from time import sleep
import os
import signal
import click
import time
import sys


class ProcessList(object):
    talent: Talent
    supervisor: Supervisor


class DaemonCFG(object):
    pid_store: str


class GlobalConfig(object):
    _version = 0.1

    daemon_config: DaemonCFG
    talent_config: TalentCFG
    supervisor_config: SupervisorCFG

    def __init__(self, config: dict):
        try:
            if self._version != float(config['version']):
                raise ValueError("Class Version: %s != Config Version: %s" % (self._version, config['version']))
            self.daemon_config = DaemonCFG()
            self.daemon_config.pid_store = config['daemon_config']['pid_store']
            self.talent_config = TalentCFG()
            self.talent_config.worker_id = config['talent_config']['worker_id']
            self.talent_config.db_file = config['talent_config']['db_file']
            self.talent_config.overlord = config['talent_config']['overlord']
            self.talent_config.grpc_port = int(config['talent_config']['grpc_port'])
            self.supervisor_config = SupervisorCFG()
            self.supervisor_config.sock_path = config['supervisor_config']['sock_path']
            self.supervisor_config.grpc_host = config['supervisor_config']['grpc_host']
            self.supervisor_config.sleep_time = int(config['supervisor_config']['sleep_time'])
            self.supervisor_config.plot_process_config = PlotProcessCFG()
            self.supervisor_config.plot_process_config.bin = config['supervisor_config']['plot_process_config']['bin']
            self.supervisor_config.plot_process_config.waiting = int(config['supervisor_config']['plot_process_config']['waiting'])
            self.supervisor_config.plot_process_config.cache1 = list()
            for _cache1 in config['supervisor_config']['plot_process_config']['cache1']:
                # print(_cache1)
                cache_cfg = CacheCFG()
                cache_cfg.dest = _cache1['dest']
                cache_cfg.capacity = _cache1['capacity']
                self.supervisor_config.plot_process_config.cache1.append(cache_cfg)
            # print(self.supervisor_config.plot_process_config.cache1)
            self.supervisor_config.plot_process_config.cache2 = list()
            for _cache2 in config['supervisor_config']['plot_process_config']['cache2']:
                cache_cfg = CacheCFG()
                cache_cfg.dest = _cache2['dest']
                cache_cfg.capacity = _cache2['capacity']
                self.supervisor_config.plot_process_config.cache2.append(cache_cfg)
            self.supervisor_config.plot_process_config.dests = config['supervisor_config']['plot_process_config']['dests']
        except (KeyError, ValueError) as e:
            raise RuntimeError("Config error, %s" % str(e))
    

def start_talent(global_config: GlobalConfig):
    _cfg = global_config.talent_config
    # print(_cfg)
    _talent = Talent(_cfg, debug=True)
    _talent.daemon = True
    _talent.start()
    return _talent


def start_supervisor(global_config: GlobalConfig):
    _cfg = global_config.supervisor_config
    # print(_cfg.plot_process_config.cache1)
    _supervisor = Supervisor(_cfg, debug=True)
    _supervisor.daemon = True
    _supervisor.start()
    return _supervisor


@click.group()
@click.option('-c', "--conf", default='config/config.yaml', help="Set config file")
@click.option('-d', '--daemon', default=True, help='Run owl daemonize')
@click.pass_context
def cli(ctx, conf, daemon):
    # click.echo(conf)
    # click.echo(daemon)
    ctx.ensure_object(dict)
    config = load_cfg(conf)
    # print(config)
    ctx.obj['config'] = GlobalConfig(config)
    ctx.obj['daemon'] = daemon


@cli.command()
@click.pass_context
def start(ctx):
    start_daemon(ctx.obj['config'], ctx.obj['daemon'])


@cli.command()
@click.pass_context
def stop(ctx):
    stop_daemon(ctx.obj['config'])


@cli.command()
@click.pass_context
def restart(ctx):
    stop_daemon(ctx.obj['config'])
    print("Ready to start ....")
    time.sleep(3)
    start_daemon(ctx.obj['config'], ctx.obj['daemon'])


def stop_daemon(config):
    _main_pid = "%s/daemon.pid" % config.daemon_config.pid_store
    if os.path.exists(_main_pid):
        with open(_main_pid) as _f:
            os.kill(int(_f.read()), signal.SIGTERM)
            print("Stop success")
    else:
        print('Not running', file=sys.stderr)


def start_daemon(config, daemon=False):
    print("For testing and debug")
    # Daemon
    _main_pid = "%s/daemon.pid" % config.daemon_config.pid_store
    if daemon:
        daemonize(_main_pid)
    process_list = ProcessList()

    def terminate(*args, **kwargs):
        print("Main - stopping supervisor")
        os.kill(process_list.supervisor.pid, signal.SIGTERM)
        while process_list.supervisor.is_alive():
            sleep(1)
        # sleep(10)
        print("Main - stopping talent")
        os.kill(process_list.talent.pid, signal.SIGTERM)
        print("Main waiting for all processes exit.")
        while process_list.talent.is_alive():
            sleep(1)
        if os.path.exists(_main_pid):
            print("Main remove pid: %s" % _main_pid)
            os.remove(_main_pid)
        print("Main exit 0")
        raise SystemExit(0)
    
    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)
    
    process_list.talent = start_talent(config)
    sleep(1)
    while not process_list.talent.is_alive():
        sleep(1)
    process_list.supervisor = start_supervisor(config)

    # process_list.supervisor.join()
    # process_list.talent.join()
    
    try:
        while True:
            # print("Talent is alive? %s" % process_list.talent.is_alive())
            # print("Supervisor is alive? %s" % process_list.supervisor.is_alive())
            if not process_list.supervisor.is_alive():
                print("Supervisor not alive, restart it")
                if not process_list.talent.is_alive():
                    print("Talent not alive, restart it")
                    process_list.talent = start_talent()
                    sleep(1)
                    while not process_list.talent.is_alive():
                        sleep(1)
                process_list.supervisor = start_supervisor(config)
            if not process_list.talent.is_alive():
                print("Talent not alive, restart it")
                process_list.talent = start_talent(config)
                sleep(1)
            sleep(10)
    except KeyboardInterrupt:
        terminate()


if __name__ == '__main__':
    cli(obj={})
    cli.add_command(start)
    cli.add_command(stop)
    cli.add_command(restart)
