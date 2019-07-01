# Python application + Statsd exporter + Prometheus + Kubernetes

First, we need to setup a local kubernetes cluster. [minikube](https://github.com/kubernetes/minikube)
is a good option.

See `src` for the application code.

## Building Docker images

We want to use the docker engine running inside the `minikube` VM:

```
$ eval $(minikube docker-env)
```


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
CMD uwsgi --http :5000  --manage-script-name --mount /myapplication=flask_app_1:app --enable-threads --processes 5
```

The last statement shows how we are running the application via `uwsgi` with 5
worker processes.

To build the image:

```
$ docker build -t amitsaha/flask_app_1 -f Dockerfile.py3 .
```

The repository also has a dockerfile to build a custom prometheus image to make
it easy to have our own target configuration:

```
$ docker build -t amitsaha/prometheus -f Dockerfile.prom .
```

## Bringing up the web application, along with prometheus, grafana and statsd

We will now run `kubectl`:

```
$ kubectl apply -f k8s_application.yaml -f k8s_infra.yaml
```

Next, we will expose the different services:

```
$ kubectl expose deployment prometheus --type=NodePort
$ kubectl expose deployment flaskapp --type=NodePort
$ kubectl expose deployment grafana --type=NodePort
```

We can obtain the exposed services' URLs via:

```
$ minikube service list
|----------------------|----------------------|-----------------------------|
|      NAMESPACE       |         NAME         |             URL             |
|----------------------|----------------------|-----------------------------|
| default              | flaskapp             | http://192.168.39.211:30630 |
| default              | flaskappsvc          | No node port                |
| default              | grafana              | http://192.168.39.211:30649 |
| default              | grafanasvc           | No node port                |
| default              | kubernetes           | No node port                |
| default              | prometheus           | http://192.168.39.211:32143 |
| default              | prometheussvc        | No node port                |
```

