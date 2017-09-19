# -*- coding: utf-8 -*-
"""
Execution script
"""

import settings
import logging
from .tracing import init_opentracing_tracer


def _set_logging(log_conf):
    import logging
    reload(logging)  # prevents process freeze when logging._lock is acquired by the parent process when fork starts
    import logging.config
    logging.config.dictConfig(log_conf)


def start_worker(tracer_name='', log_level=logging.DEBUG, **kwargs):
    """
    A simple wrapper for workflow.start_worker(role) , needed to solve the logger import problem with multiprocessing
    :param role: one of the constants workflow.ROLE_...
    :return:
    """
    _set_logging(settings.LOGGING)

    init_opentracing_tracer(tracer_name, log_level)

    import workflow

    workflow.start_worker_for_queue(**kwargs)