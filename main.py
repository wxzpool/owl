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

if __name__ == '__main__':
    print("For testing and debug")
    cfg = supervisor.SupervisorCFG()
    cfg.sock_path = "/tmp"
    server = supervisor.Supervisor(cfg, debug=True)
    server.start()
