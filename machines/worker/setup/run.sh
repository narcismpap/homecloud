#!/bin/sh

# HomeCloud
# > Worker > Docker Entrypoint
#
# Author: Narcis.IO <n@narcis.io>

uwsgi \
    --plugin /usr/lib/uwsgi/python_plugin.so \
    --socket 0.0.0.0:8000 \
    --chdir /homecloud/code/ \
    --pythonpath /usr/local/lib/python2.7/site-packages \
    --wsgi-file /homecloud/code/wsgi.py \
    --master \
    --protocol http \
    --uid homecloud\
    --gid nobody\
    --processes 4 \
    --threads 2 \
    --need-app
