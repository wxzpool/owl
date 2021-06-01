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
import subprocess
from time import sleep
import os
import signal
import click
import time
import sys

# todo 这个文件要重写


def start_talent(_config):
    pass


def start_supervisor(_config):
    pass


@click.group()
@click.option("--conf", default='config/config.yaml', help="Set config file, default=config/config.yaml")
@click.option('--daemon', default=True, help='Run owl daemonize, default=True')
@click.pass_context
def cli(ctx, conf, daemon):
    # click.echo(conf)
    ctx.obj['config_file'] = conf
    # click.echo(daemon)
    ctx.ensure_object(dict)
    config = load_cfg(conf)
    # print(config)
    ctx.obj['talent_pid'] = config['talent_config']['']
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
