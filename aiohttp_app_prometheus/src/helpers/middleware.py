from prometheus_client import Counter, Gauge, Histogram, CONTENT_TYPE_LATEST
import prometheus_client
import time
import asyncio

from aiohttp import web

def prom_middleware(app_name):
    @asyncio.coroutine
    def factory(app, handler):
        @asyncio.coroutine
        def middleware_handler(request):
            try:
                request['start_time'] = time.time()
                request.app['REQUEST_IN_PROGRESS'].labels(
                            app_name, request.path, request.method).inc()
                response = yield from handler(request)
                resp_time = time.time() - request['start_time']
                request.app['REQUEST_LATENCY'].labels(app_name, request.path).observe(resp_time)
                request.app['REQUEST_IN_PROGRESS'].labels(app_name, request.path, request.method).dec()
                request.app['REQUEST_COUNT'].labels(
                            app_name, request.method, request.path, response.status).inc()
                return response
            except Exception as ex:
                raise
        return middleware_handler
    return factory


async def metrics(request):
    resp = web.Response(body=prometheus_client.generate_latest())
    resp.content_type = CONTENT_TYPE_LATEST
    return resp


def setup_metrics(app, app_name):
    app['REQUEST_COUNT'] = Counter(
      'requests_total', 'Total Request Count',
      ['app_name', 'method', 'endpoint', 'http_status']
    )
    app['REQUEST_LATENCY'] = Histogram(
        'request_latency_seconds', 'Request latency',
        ['app_name', 'endpoint']
    )

    app['REQUEST_IN_PROGRESS'] = Gauge(
        'requests_in_progress_total', 'Requests in progress',
        ['app_name', 'endpoint', 'method']
    )

    app.middlewares.insert(0, prom_middleware(app_name))
    app.router.add_get("/metrics", metrics)

@asyncio.coroutine
def error_middleware(app, handler):

    @asyncio.coroutine
    def middleware_handler(request):
        try:
            response = yield from handler(request)
            return response
        except web.HTTPException as ex:
            resp = web.Response(body=str(ex), status=ex.status)
            return resp
        except Exception as ex:
            resp = web.Response(body=str(ex), status=500)
            return resp



    return middleware_handler
