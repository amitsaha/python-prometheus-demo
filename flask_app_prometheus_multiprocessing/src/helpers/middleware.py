from flask import request, Response
from prometheus_client import Counter, Histogram
import time
import sys
import prometheus_client
from prometheus_client import multiprocess, CollectorRegistry

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status'],
    registry=registry,
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint'],
    registry=registry,
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('webapp', request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('webapp', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)

    @app.route('/metrics')
    def metrics():
        return Response(prometheus_client.generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)


