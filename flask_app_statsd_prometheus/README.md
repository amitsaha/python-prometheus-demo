## Building Docker image

Python 3:

```
$ docker build -t amitsaha/flask_app_statsd -f Dockerfile.py3 .
```

Python 2:

```
$ docker build -t amitsaha/flask_app_statsd -f Dockerfile.py2 .
```

## Running the application

```
$ docker run -P amitsaha/flask_app_statsd

$ docker ps # will show the mapped port on the host
```

## Bringing up the web application, along with prometheus

```
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

## Updating the web app started via `docker compose`

```
$ docker-compose up -d --no-deps webapp
```
