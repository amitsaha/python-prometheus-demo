# Example Flask application with Prometheus monitoring

See ``src`` for the application code. The difference from [flask_app_prometheus](https://github.com/amitsaha/python-prometheus-demo/tree/master/flask_app_prometheus) is that the metrics add an additional label:
`worker_id` to the metrics. This basically means that when running
under `uwsgi` or `gunicorn`, the label will make each scrape that
is answered by a different worker an entirely different metric. 

However, this doesn't completely solve the problem of having 
inconsistent value for a metric depending on which worker responds
to the HTTP request from prometheus. 

To explain what I mean - let's say we have a counter metric `request_count`. This is the number of requests served by the
web application. Now consider, two time windows: `t1-t2` and `t2-t3`.
Ideally, if we have N workers, requests to our web application will
be served such that requests over a time window are equally distributed
among the N workers. However, that *may* eventually be true over
a large number of requests. However, there's nothing preventing a
single worker serving all 100 requests in the time window `t1-t2`
and a different worker serving all 50 requests in the time window
`t2-t3`. If you now do `sum(request_count) by (instance)` (for example)
you will see the value of the counter as decreasing.


In addition, this leads to a proliferation of metrics: 
for a single metric we now have `# of workers x metric` number of 
metrics per application instance. 


## Building Docker image

The Python 3 based [Dockerfile](Dockerfile.py3) uses an Alpine Linux base image
and expects the application source code to be volume mounted at `/application`
when run:

```
FROM python:3.6.1-alpine
ADD . /application
WORKDIR /application
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip install -r src/requirements.txt; \
	apk del .build-deps;
EXPOSE 5000
VOLUME /application
CMD uwsgi --http :5000  --manage-script-name --mount /myapplication=flask_app:app --enable-threads --processes 5
```

The last statement shows how we are running the application via `uwsgi` with 5
worker processes.

To build the image:

```
$ docker build -t amitsaha/flask_app -f Dockerfile.py3 .
```

## Running the application

We can just run the web application as follows:

```
$ docker run  -ti -p 5000:5000 -v `pwd`/src:/application amitsaha/flask_app
```

## Bringing up the web application, along with prometheus

The [docker-compse.yml](docker-compose.yml) brings up the `webapp` service which is our web application
using the image `amitsaha/flask_app` we built above. The [docker-compose-infra.yml](docker-compose-infra.yml)
file brings up the `prometheus` service and also starts the `grafana` service which
is available on port 3000. The config directory contains a `prometheus.yml` file
which sets up the targets for prometheus to scrape. The scrape configuration 
looks as follows:

```
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
         - targets: ['localhost:9090']
  - job_name: 'webapp'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
        - targets: ['webapp:5000']
```

Prometheus scrapes itself, which is the first target above. The second target
is the our web application on port 5000.
Since these services are running via `docker-compose`, `webapp` automatically resolves to the IP of the webapp container. 

To bring up all the services:

```
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

