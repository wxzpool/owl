#!/usr/bin/env python
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
from libs.sturcts import ApiCFG
from libs import api
import os
import sys
import click
import time
import signal
import multiprocessing as mp


@click.group()
@click.option("--conf", default='config/config.yaml', help="Set config file, default=config/config.yaml")
@click.option('--daemon', default=True, help='是否后台执行, default=True')
@click.option("--debug", default=False, help="debug模式， default=False")
@click.pass_context
def cli(ctx, conf, daemon, debug):
    # click.echo(conf)
    # click.echo("daemon: %s" % daemon)
    # click.echo('debug: %s' % debug)
    ctx.ensure_object(dict)
    # print(config)
    config = load_cfg(conf)
    ctx.obj['daemon'] = daemon
    ctx.obj['debug'] = debug

    try:
        api.app.config.update({
            "grpc_host": config['supervisor_config']['grpc_host'],
            "worker_id": config['talent_config']['worker_id'],
        })
        ctx.obj['pid'] = config['api_config']['pid_file']
        ctx.obj['config'] = ApiCFG()
        ctx.obj['config'].listen = config['api_config']['listen']
        ctx.obj['config'].port = int(config['api_config']['port'])
        ctx.obj['config'].threaded = config['api_config']['threaded']
        ctx.obj['config'].pid_file = config['api_config']['pid_file']
        ctx.obj['config'].log_file = config['api_config']['log_file']
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


def start_daemon(pid, config: ApiCFG, daemon: bool, debug: bool):
    # target = Supervisor(config, debug=debug, pid=pid)

    # daemonize(pid, daemon)

    wsgi_app_cfg = {
        "host": config.listen,
        "port": config.port,
        "debug": debug,
        "threaded": config.threaded
    }
    #
    # wsgi_app = mp.Process(target=api.app.run, kwargs=wsgi_app_cfg)
    # wsgi_app.daemon = daemon
    #
    # wsgi_app.start()
    #
    # wsgi_app.join()
    api.app.run(**wsgi_app_cfg)


if __name__ == '__main__':
    cli(obj={})
    cli.add_command(start)
    cli.add_command(stop)
    cli.add_command(restart)
