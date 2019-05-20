#!/bin/sh

pwd
gunicorn --bind 0.0.0.0:8000  demo.wsgi
