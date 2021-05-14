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

from libs import log_receiver

if __name__ == '__main__':
    print("For testing and debug")
    cfg = log_receiver.LogReceiverCFG(
        name="test",
        sock_path="/tmp"
    )
    server = log_receiver.LogReceiver(cfg, debug=True)
    # server.daemon = True
    server.start()
