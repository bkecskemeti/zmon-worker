import opentracing
import logging


def init_opentracing_tracer(tracer, log_level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    logger.info('Initializing opentracing tracer: {}'.format(tracer))

    if tracer == 'instana':
        import instana.options as instana_opts  # noqa
        import instana.tracer  # noqa

        instana.tracer.init(instana_opts.Options(service='zmon-worker', log_level=log_level))

    else:
        opentracing.tracer = opentracing.Tracer()
