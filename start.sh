#!/bin/bash

/usr/local/bin/python /root/src/manage.py migrate
/usr/local/bin/python /root/src/manage.py runserver 0.0.0.0:8000
