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
import psutil
import subprocess


def start_talent(_config):
    pass


def start_supervisor(_config):
    pass


@click.group()
@click.option("--conf", default='config/config.yaml', help="Set config file, default=config/config.yaml")
@click.option('--debug', default=False, help='debug, default=False')
@click.pass_context
def cli(ctx, conf, debug):
    # click.echo(conf)
    ctx.obj['config_file'] = conf
    # click.echo(daemon)
    ctx.ensure_object(dict)
    config = load_cfg(conf)
    # print(config)
    ctx.obj['debug'] = debug
    ctx.obj['talent_pid'] = config['talent_config']['pid_file']
    ctx.obj['supervisor_pid'] = config['supervisor_config']['pid_file']
    ctx.obj['daemon_pid'] = config['daemon_config']['pid_file']
    # ctx.obj['daemon'] = daemon


@cli.command()
@click.option('-b', '--binary', default=False, help='Run bin not source, default=False')
@click.pass_context
def start(ctx, binary):
    ctx.obj['bin'] = binary
    start_daemon(ctx.obj)
    

@cli.command()
@click.pass_context
def stop(ctx):
    stop_daemon(ctx.obj)


@cli.command()
@click.pass_context
def restart(ctx):
    stop_daemon(ctx.obj)
    print("Ready to start ....")
    time.sleep(3)
    start_daemon(ctx.obj)


def stop_daemon(config):
    daemon_pid = _get_pid(config['daemon_pid'])
    os.kill(daemon_pid, signal.SIGTERM)
    

def _get_pid(pid_file) -> int:
    _pid = 0
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            try:
                _pid = int(f.read())
            except ValueError:
                pass
    return _pid


def start_daemon(config):
    # print("For testing and debug")
    # Daemon
    
    daemonize(config['daemon_pid'])

    def terminate(*args, **kwargs):
        _talent_pid = _get_pid(config['talent_pid'])
        _supervisor_pid = _get_pid(config['supervisor_pid'])
        if supervisor_pid > 0:
            os.kill(_supervisor_pid, signal.SIGTERM)
            print("Supervisor stop success")
        else:
            print('Supervisor not running')
        if talent_pid > 0:
            os.kill(_talent_pid, signal.SIGTERM)
            print("Talent stop success")
        else:
            print('Talent not running')
        raise SystemExit(0)

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)
    
    # process_list.supervisor.join()
    # process_list.talent.join()
    _start_talent(config)
    time.sleep(1)
    _start_supervisor(config)
    
    try:
        while True:
            sleep(10)
            talent_pid = _get_pid(config['talent_pid'])
            supervisor_pid = _get_pid(config['supervisor_pid'])
            # print("Talent is alive? %s" % process_list.talent.is_alive())
            # print("Supervisor is alive? %s" % process_list.supervisor.is_alive())
            if talent_pid == 0 or not psutil.pid_exists(talent_pid):
                print("Talent not alive, restart it")
                _start_talent(config)
            if supervisor_pid == 0 or not psutil.pid_exists(supervisor_pid):
                print("Supervisor not alive, restart it")
                _start_supervisor(config)
    except KeyboardInterrupt:
        terminate()


def _start_supervisor(config_file, daemon=True):
    if config_file['bin']:
        exe_cmd = "./owl_supervisor"
    else:
        exe_cmd = "./owl_supervisor.py"
    cmd = "{bin} --daemon {daemon} --debug {debug} start".format(
        bin=exe_cmd,
        daemon=daemon,
        debug=config_file['debug']
    )
    print(cmd)
    _s = subprocess.Popen(cmd, cwd=config_file['runtime_dir'], stdin=subprocess.PIPE, shell=True, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _s.wait()
    print("supervisor start finish, rt: %s" % _s.returncode)
    if _s.returncode != 0:
        print(_s.stdout.read())
        print(_s.stderr.read())


def _start_talent(config_file, daemon=True):
    if config_file['bin']:
        exe_cmd = "./owl_talent"
    else:
        exe_cmd = "./owl_talent.py"
    cmd = "{bin} --daemon {daemon} --debug {debug} start".format(
        bin=exe_cmd,
        daemon=daemon,
        debug=config_file['debug']
    )
    print(cmd)
    _s = subprocess.Popen(cmd, cwd=config_file['runtime_dir'], stdin=subprocess.PIPE, shell=True, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _s.wait()
    print("talent start finish, rt: %s" % _s.returncode)
    if _s.returncode != 0:
        print(_s.stdout.read())
        print(_s.stderr.read())


if __name__ == '__main__':
    # print(os.getcwd())
    # print(os.path.abspath(os.path.dirname(sys.argv[0])))
    target_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    # os.chdir(target_dir)
    # raise RuntimeError
    cli(obj={"runtime_dir": target_dir})
    cli.add_command(start)
    cli.add_command(stop)
    cli.add_command(restart)
