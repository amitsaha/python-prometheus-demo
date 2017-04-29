# Example Flask application

See ``src`` for the application code.

## Building Docker image

Python 3:

```
$ docker build -t amitsaha/flask_app -f Dockerfile.py3 .
```

## Running the application

```
$ docker run  -ti -p 5000:5000 -v `pwd`/src:/application amitsaha/flask_app
```

## Bringing up the web application, along with prometheus

```
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

## Updating the web app started via `docker compose`

```
$ docker-compose up -d --no-deps webapp
```
