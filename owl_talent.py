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
from libs.talent import Talent, TalentCFG


@click.group()
@click.option("--conf", default='config/config.yaml', help="Set config file, default=config/config.yaml")
@click.option('--daemon', default=True, help='是否后台执行, default=True')
@click.option("--debug", default=False, help="debug模式， default=False")
@click.pass_context
def cli(ctx, conf, daemon, debug):
    click.echo("daemon: %s" % daemon)
    click.echo('debug: %s' % debug)
    ctx.ensure_object(dict)
    config = load_cfg(conf)
    # print(config)
    config = load_cfg(conf)
    ctx.obj['daemon'] = daemon
    ctx.obj['debug'] = debug
    try:
        ctx.obj['pid'] = config['talent_config']['pid_file']
        ctx.obj['config'] = TalentCFG()
        ctx.obj['config'].log_file = config['talent_config']['log_file']
        ctx.obj['config'].pid_file = config['talent_config']['pid_file']
        ctx.obj['config'].supervisor_pid = config['supervisor_config']['pid_file']
        ctx.obj['config'].worker_id = config['talent_config']['worker_id']
        ctx.obj['config'].db_file = config['talent_config']['db_file']
        ctx.obj['config'].overlord = config['talent_config']['overlord']
        ctx.obj['config'].grpc_port = int(config['talent_config']['grpc_port'])
        
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
    target = Talent(config, debug=debug, pid=pid)

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

