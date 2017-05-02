# Python + Prometheus Demo

## Contents

The following two applications are discussed in the first part of the blog post:

### [flask_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_promethus)

A Flask application using the native Prometheus Python client to expose metrics via the `/metrics` endpoint

### [flask_app_statsd_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_statsd_promethus)

A Flask application which pushes the metrics to a `statsd` bridge which converts `DogStatsd` metrics to `Prometheus` compatible metrics.
