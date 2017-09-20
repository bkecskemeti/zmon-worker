import opentracing
import logging


def init_opentracing_tracer(tracer, log_level=logging.DEBUG):
    if tracer == 'instana':
        import instana.options as instana_opts  # noqa
        import instana.tracer  # noqa

        instana.tracer.init(instana_opts.Options(service='zmon-worker', log_level=log_level))
    elif tracer == 'basic':
        from basictracer import BasicTracer  # noqa

        opentracing.tracer = BasicTracer()

    else:
        opentracing.tracer = opentracing.Tracer()
