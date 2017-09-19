#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Server module for exposing an rpc interface for clients to remotely control a local ProcessManager
"""

import sys
import signal
import settings
import logging

from process_controller import ProcessController
import worker
import rpc_utils

from .flags import MONITOR_RESTART, MONITOR_KILL_REQ, MONITOR_PING


def sigterm_handler(signum, frame):
    # this will propagate the SystemExit exception all around, so we can quit listening loops, cleanup and exit
    sys.exit(0)


class ProcessControllerProxy(rpc_utils.RpcProxy):
    """
    A proxy class to expose some methods of multiprocess manager server to listen to remote requests,
    possible request are:
     1. start N more child processes
     2. terminate processes with pid1, pid2, ...
     3. report running statistics
     4. report status of process with pid1
     5. terminate all child processes
     6. terminate yourself
    """

    exposed_obj_class = ProcessController

    valid_methods = ['spawn_many', 'list_running', 'list_stats', 'start_action_loop', 'stop_action_loop',
                     'is_action_loop_running', 'get_dynamic_num_processes', 'set_dynamic_num_processes',
                     'get_action_policy', 'set_action_policy', 'available_action_policies', 'terminate_all_processes',
                     'terminate_process', 'mark_for_termination', 'ping', 'add_events', 'processes_view', 'status_view',
                     'health_state', 'single_process_view']

    def on_exit(self):
        self.get_exposed_obj().terminate_all_processes()


class MainProcess(object):

    def __init__(self, tracer_name='', log_level=logging.DEBUG):
        self.tracer_name = tracer_name
        self.log_level = log_level

        signal.signal(signal.SIGTERM, sigterm_handler)

    def start_proc_control(self):
        self.proc_control = ProcessController(default_target=worker.start_worker,
                                              default_args=(self.tracer_name, self.log_level),
                                              default_flags=MONITOR_RESTART | MONITOR_KILL_REQ | MONITOR_PING)

    def start_rpc_server(self):

        rpc_proxy = ProcessControllerProxy(self.proc_control)

        rpc_utils.start_RPC_server(settings.RPC_SERVER_CONF['HOST'],
                                   settings.RPC_SERVER_CONF['PORT'],
                                   settings.RPC_SERVER_CONF['RPC_PATH'],
                                   rpc_proxy)
