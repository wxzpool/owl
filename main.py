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

if __name__ == '__main__':
    print("For testing and debug")
    # cfg = supervisor.SupervisorCFG()
    # cfg.sock_path = "/tmp"
    # server = supervisor.Supervisor(cfg, debug=True)
    # server.start()
    cfg = talent.TalentCFG()
    cfg.db_file = "/tmp/owl/talent.db"
    talent_server = talent.Talent(cfg, debug=True)
    # talent_server.daemon = True
    talent_server.start()

