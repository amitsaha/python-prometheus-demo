# Example Django application

See `src` for the application code and top level README for the description of this repo from a functionality
point of view.


## Building Docker image

The Python 3 based [Dockerfile](Dockerfile.py3) uses an Alpine Linux base image
and expects the application source code to be volume mounted at `/application`
when run:

```
FROM python:3.7-alpine
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
EXPOSE 8000
VOLUME /application

CMD gunicorn --bind 0.0.0.0:8000  demo.wsgi
```

The last statement shows how we are running the application via `gunicorn` with 5
worker processes.

To build the image:

```
$ docker build -t amitsaha/django_app_2 -f Dockerfile.py3 .
```

## Running the application

We can just run the web application as follows:

```
$ docker run  -ti -p 8000:8000 -v `pwd`/src:/application amitsaha/django_app_2
```

## Bringing up the web application, along with prometheus

The [docker-compse.yml](docker-compose.yml) brings up the `webapp` service which is our web application
using the image `amitsaha/flask_app_1` we built above. The [docker-compose-infra.yml](docker-compose-infra.yml)
file brings up the `statsd` service which is the statsd exporter, `prometheus` service and also starts the `grafana` service which
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
        - targets: ['statsd:9102']

```

Prometheus scrapes itself, which is the first target above. The second target
is the statsd exporter on port 9102.

Since these services are running via `docker-compose`, `statsd` automatically resolves to the IP of the statsd exporter container.

To bring up all the services:

```
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

