from flask import Flask, request, Response
from flask_datadog import StatsD

app = Flask(__name__)
app.config['STATSD_HOST'] =  'statsd-exporter'
app.config['STATSD_PORT'] = 9125
app.config['DATADOG_RESPONSE_METRIC_NAME'] = 'demo_webapp.response.time'
app.config['STATSD_USEMS'] = True

# custom tag
app.config['STATSD_TAGS'] = ['version:0.1']

statsd = StatsD(app)

@app.route('/test')
def test():
    return 'rest'

@app.route('/test1')
def test1():
    1/0
    return 'rest'


@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

if __name__ == '__main__':
    app.run()
