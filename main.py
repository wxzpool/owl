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

from libs import supervisor
from libs import talent
from libs.daemon import daemonize
from time import sleep
import os
import signal


class ProcessList(object):
    talent: talent.Talent
    supervisor: supervisor.Supervisor


if __name__ == '__main__':
    
    print("For testing and debug")
    # Daemon
    daemonize()
    process_list = ProcessList()

    def terminate(*args, **kwargs):
        print("Main - stopping supervisor")
        os.kill(process_list.supervisor.pid, signal.SIGTERM)
        print("Main - stopping talent")
        os.kill(process_list.talent.pid, signal.SIGTERM)
        print("Main waiting for all processes exit.")
        while process_list.supervisor.is_alive() or process_list.talent.is_alive():
            sleep(1)
        print("Main exit 0")
        raise SystemExit(0)
    
    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)
    
    cfg = talent.TalentCFG()
    cfg.db_file = "/tmp/owl/talent.db"
    process_list.talent = talent.Talent(cfg, debug=True)
    process_list.talent.daemon = True
    process_list.talent.start()
    sleep(1)
    while not process_list.talent.is_alive():
        sleep(1)
    cfg = supervisor.SupervisorCFG()
    cfg.sock_path = "/tmp"
    process_list.supervisor = supervisor.Supervisor(cfg, debug=True)
    process_list.supervisor.daemon = True
    process_list.supervisor.start()

    # process_list.supervisor.join()
    # process_list.talent.join()
    
    try:
        while True:
            print("Talent is alive? %s" % process_list.talent.is_alive())
            print("Supervisor is alive? %s" % process_list.supervisor.is_alive())
            sleep(10)
    except KeyboardInterrupt:
        terminate()
