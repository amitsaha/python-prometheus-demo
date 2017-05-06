from prometheus_client import Counter, Gauge, Histogram
import time
import asyncio

from aiohttp import web


REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

REQUEST_IN_PROGRESS = Gauge('requests_in_progress', 'Requests in progress',
    ['app_name', 'endpoint', 'method']
)

def prom_middleware(app_name):
  @asyncio.coroutine
  def factory(app, handler):

      @asyncio.coroutine
      def middleware_handler(request):
          try:
              request['start_time'] = time.time()
              REQUEST_IN_PROGRESS.labels(app_name, request.path, request.method).inc()
              response = yield from handler(request)
              resp_time = time.time() - request['start_time']
              REQUEST_LATENCY.labels(app_name, request.path).observe(resp_time)
              REQUEST_IN_PROGRESS.labels(app_name, request.path, request.method).dec()
              REQUEST_COUNT.labels(app_name, request.method, request.path, response.status).inc()
              return response
          except Exception as ex:
              raise
      return middleware_handler
  return factory

def setup_metrics(app, app_name):
  app.middlewares.insert(0, prom_middleware(app_name))

@asyncio.coroutine
def error_middleware(app, handler):

    @asyncio.coroutine
    def middleware_handler(request):
        try:
            response = yield from handler(request)
            return response
        except Exception as ex:
            resp = web.Response(body=str(ex), status=500)
            return resp
        except web.HTTPException as ex:
            resp = web.Response(body=str(ex), status=ex.status)
            return resp
    return middleware_handler
