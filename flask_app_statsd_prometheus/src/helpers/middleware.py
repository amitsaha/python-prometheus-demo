from flask import request
from datadog import DogStatsd
import time
import sys


statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'
REQUEST_COUNT_METRIC_NAME = 'request_count'

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    statsd.histogram(REQUEST_LATENCY_METRIC_NAME,
            resp_time,
            tags=[
                'service:webapp',
                'endpoint: %s' % request.path,
                ]
    )
    return response

def record_request_data(response):
    statsd.increment(REQUEST_COUNT_METRIC_NAME,
            tags=[
                'service: webapp', 
                'method: %s' % request.method, 
                'endpoint: %s' % request.path,
                'status: %s' % str(response.status_code)
                ]
    )
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)
