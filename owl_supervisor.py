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
import click
import time
import os
import sys
import signal
from libs.supervisor import Supervisor, PlotProcessCFG, SupervisorCFG, CacheCFG


@click.group()
@click.option("--conf", default='config/config.yaml', help="Set config file, default=config/config.yaml")
@click.option('--daemon', default=True, help='是否后台执行, default=True')
@click.option("--debug", default=False, help="debug模式， default=False")
@click.pass_context
def cli(ctx, conf, daemon, debug):
    # click.echo(conf)
    click.echo("daemon: %s" % daemon)
    click.echo('debug: %s' % debug)
    ctx.ensure_object(dict)
    config = load_cfg(conf)
    # print(config)
    config = load_cfg(conf)
    ctx.obj['daemon'] = daemon
    ctx.obj['debug'] = debug
    try:
        ctx.obj['pid'] = config['supervisor_config']['pid_file']
        ctx.obj['config'] = SupervisorCFG()
        ctx.obj['config'].log_file = config['supervisor_config']['log_file']
        ctx.obj['config'].pid_file = config['supervisor_config']['pid_file']
        ctx.obj['config'].sock_path = config['supervisor_config']['sock_path']
        ctx.obj['config'].grpc_host = config['supervisor_config']['grpc_host']
        ctx.obj['config'].sleep_time = int(config['supervisor_config']['sleep_time'])
        ctx.obj['config'].plot_process_config = PlotProcessCFG()
        ctx.obj['config'].plot_process_config.cap_limit = config['supervisor_config']['plot_process_config']['cap_limit']
        ctx.obj['config'].plot_process_config.log_store = config['supervisor_config']['plot_process_config']['log_store']
        ctx.obj['config'].plot_process_config.bin = config['supervisor_config']['plot_process_config']['bin']
        ctx.obj['config'].plot_process_config.waiting = int(config['supervisor_config']['plot_process_config']['waiting'])
        ctx.obj['config'].plot_process_config.cache1 = list()
        # for _cache1 in config['supervisor_config']['plot_process_config']['cache1']:
        #     # print(_cache1)
        #     cache_cfg = CacheCFG()
        #     cache_cfg.dest = _cache1['dest']
        #     cache_cfg.capacity = _cache1['capacity']
        #     ctx.obj['config'].plot_process_config.cache1.append(cache_cfg)
        # # print(self.supervisor_config.plot_process_config.cache1)
        # ctx.obj['config'].plot_process_config.cache2 = list()
        # for _cache2 in config['supervisor_config']['plot_process_config']['cache2']:
        #     cache_cfg = CacheCFG()
        #     cache_cfg.dest = _cache2['dest']
        #     cache_cfg.capacity = _cache2['capacity']
        #     ctx.obj['config'].plot_process_config.cache2.append(cache_cfg)
        # ctx.obj['config'].plot_process_config.dests = config['supervisor_config']['plot_process_config']['dests']
    except (KeyError, ValueError) as e:
        raise RuntimeError("Config error, %s" % str(e))


@cli.command()
@click.pass_context
def start(ctx):
    start_daemon(ctx.obj['pid'], ctx.obj['config'], ctx.obj['daemon'], ctx.obj['debug'])


@cli.command()
@click.pass_context
def stop(ctx):
    stop_daemon(ctx.obj['pid'])


@cli.command()
@click.pass_context
def restart(ctx):
    stop_daemon(ctx.obj['pid'])
    print("Ready to start ....")
    time.sleep(3)
    start_daemon(ctx.obj['pid'], ctx.obj['config'], ctx.obj['daemon'], ctx.obj['debug'])


def stop_daemon(pid):
    if os.path.exists(pid):
        with open(pid) as _f:
            os.kill(int(_f.read()), signal.SIGTERM)
            print("Stop success")
    else:
        print('Not running', file=sys.stderr)


def start_daemon(pid, config, daemon, debug):
    target = Supervisor(config, debug=debug, pid=pid)

    daemonize(pid, daemon)
    
    try:
        target.run()
    except InterruptedError:
        pass


if __name__ == '__main__':
    cli(obj={})
    cli.add_command(start)
    cli.add_command(stop)
    cli.add_command(restart)

