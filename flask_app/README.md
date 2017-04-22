## Building Docker image

Python 3:

```
$ docker build -t amitsaha/flask_app -f Dockerfile.py3 .
```

Python 2:

```
$ docker build -t amitsaha/flask_app -f Dockerfile.py2 .
```

## Running the application

```
$ docker run -P amitsaha/flask_app

$ docker ps # will show the mapped port on the host
```
