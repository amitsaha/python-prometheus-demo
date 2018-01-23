from flask import request
from prometheus_client import Counter, Histogram
import time
import sys
try:
    import uwsgi
    use_uwsgi_worker_id = True
except ImportError:
    import os
    use_uwsgi_worker_id = False


REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status', 'worker_id']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint', 'worker_id']
)

def _get_worker_id():
    if use_uwsgi_worker_id:
        worker_id = uwsgi.worker_id()
    else:
        worker_id = os.getpid()
    return worker_id

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('webapp', request.path, _get_worker_id()).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('webapp', request.method, request.path,
            response.status_code, _get_worker_id()).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)
