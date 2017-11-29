# -*- coding: utf-8 -*-
"""
Execution script
"""

import settings
import logging
from opentracing_utils import init_opentracing_tracer, trace_requests

# Trace all outgoing HTTP calls via requests lib
trace_requests()


def _set_logging(log_conf):
    import logging
    reload(logging)  # prevents process freeze when logging._lock is acquired by the parent process when fork starts
    import logging.config
    logging.config.dictConfig(log_conf)


def start_worker(tracer_name='', tracer_key='', log_level=logging.DEBUG, **kwargs):
    """
    A simple wrapper for workflow.start_worker(role) , needed to solve the logger import problem with multiprocessing
    :param role: one of the constants workflow.ROLE_...
    :return:
    """
    _set_logging(settings.LOGGING)

    tracer_port = kwargs.get('tracer_port')
    tracer_port = int(tracer_port) if tracer_port else None

    logger = logging.getLogger(__name__)
    logger.info('OPENTRACING: tracer={} host={} port={}'.format(tracer_name, kwargs.get('tracer_host'), tracer_port))

    init_opentracing_tracer(
        tracer_name, component_name='zmon-worker', access_token=tracer_key, collector_host=kwargs.get('tracer_host'),
        collector_port=tracer_port, verbosity=kwargs.get('tracer_verbosity'))

    import workflow

    workflow.start_worker_for_queue(**kwargs)
