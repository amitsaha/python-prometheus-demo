# Python + Prometheus Demo

## Demos based on codeship blog posts

The following two applications are discussed in the [first blog post](https://www.cloudbees.com/blog/monitoring-your-synchronous-python-web-applications-using-prometheus?utm_content=58060028&utm_medium=social&utm_source=twitter):

### [flask_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus)

A Flask application using the native Prometheus Python client to expose metrics via the `/metrics` endpoint

### [flask_app_statsd_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_statsd_prometheus)

A Flask application which pushes the metrics to a `statsd` bridge which converts `DogStatsd` metrics to `Prometheus` compatible metrics.

The [second blog post](https://t.co/AmQn2rxetI) refers to the next application:

### [aiohttp_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/aiohttp_app_prometheus)

An aiohttp application with prometheus integeration.

## Django web application + statsd -> Prometheus

### [django_app_statsd_prometheus](./django_app_statsd_prometheus)

This demo demonstrates how we can push HTTP metrics from a Django application into statsd exporter
which is then scraped by prometheus.

### [django_app_gunicorn_statsd_prometheus](./django_app_gunicorn_statsd_prometheus)

This demo demonstrates howe can push statsd metrics from gunicorn running a django application.
I learned about this approach from this [blog post](https://medium.com/@damianmyerscough/monitoring-gunicorn-with-prometheus-789954150069).


## Attempts to get native prometheus export working

See [blog post](http://echorand.me/your-options-for-monitoring-multi-process-python-applications-with-prometheus.html)

### [flask_app_prometheus_worker_id](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus_worker_id)

### [flask_app_prometheus_multiprocessing](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus_multiprocessing)


