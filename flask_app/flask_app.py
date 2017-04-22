from flask import Flask, request, Response
import prometheus_client
from prometheus_client import start_http_server, Counter

REQUEST_COUNT = Counter('request_count', 'App Request Count',
        ['app_name', 'method', 'endpoint', 'http_status'])
app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

@app.after_request
def increment_request_count(response):
    REQUEST_COUNT.labels('test_app', request.method, request.path,
            response.status_code).inc()
    return response


# Expose a metrics endpoint to return
# prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(),
            mimetype=CONTENT_TYPE_LATEST)

@app.route('/test')
def test():
    return 'rest'

if __name__ == '__main__':
    app.run(debug=True)
