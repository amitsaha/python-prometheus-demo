import time
from datadog import DogStatsd
import time
import sys


statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'
REQUEST_COUNT_METRIC_NAME = 'request_count'

class StatsdReporter():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        response = self.get_response(request)
        #FIXME: https://docs.djangoproject.com/en/2.2/ref/request-response/
        print("Statsd middleware: request {0} {1}".format(request.path_info, request.method))
        if response:
            resp_time = time.time() - request.start_time
            statsd.histogram(REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                tags=[
                    'service:webapp',
                    'endpoint: %s' % request.path_info,
                ]
            )
            statsd.increment(REQUEST_COUNT_METRIC_NAME,
                tags=[
                    'service: webapp', 
                    'method: %s' % request.method, 
                    'endpoint: %s' % request.path_info,
                    'status: %s' % str(response.status_code)
                ]
            )
        return response
