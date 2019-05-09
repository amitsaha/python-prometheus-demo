import time
# FIXME: integrate with datadogpy

class StatsdReporter():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        response = self.get_response(request)
        #FIXME: https://docs.djangoproject.com/en/2.2/ref/request-response/
        print("Statsd middleware: request {0} {1}".format(request.path_info, request.method))
        if response:
            request_time = time.time() - request.start_time
            print("Statsd middleware: request {0} {1} took {2} seconds (HTTP response: {3})".format(request.path_info, request.method, request_time, response.status_code))
        import sys; sys.stdout.flush()
        return response
