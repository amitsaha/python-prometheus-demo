# Example Flask application

See ``src`` for the application code.

## Building Docker image

Python 3:

```
$ docker build -t amitsaha/flask_app_1 -f Dockerfile.py3 .
```

## Running the application

```
$ docker run  -ti -p 5000:5000 -v `pwd`/src:/application amitsaha/flask_app_1
```

## Bringing up the web application, along with prometheus

```
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

## Updating the web app started via `docker compose`

```
$ docker-compose up -d --no-deps webapp
```

# Troubleshooting

If you see errors when you make requests to the web application stating that
no application could be found, run `docker rm webapp` to remove the web application
service and run `docker-compose up` as per above.
