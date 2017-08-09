# Python + Prometheus Demo

## Contents

The following two applications are discussed in the [first blog post](https://t.co/7mUox6RZas):

### [flask_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus)

A Flask application using the native Prometheus Python client to expose metrics via the `/metrics` endpoint

### [flask_app_statsd_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_statsd_prometheus)

A Flask application which pushes the metrics to a `statsd` bridge which converts `DogStatsd` metrics to `Prometheus` compatible metrics.

The [second blog post](https://t.co/AmQn2rxetI) refers to the next application:

### [aiohttp_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/aiohttp_app_prometheus)

An aiohttp application with prometheus integeration.
