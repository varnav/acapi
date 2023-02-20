#!/bin/bash

nginx -t
nginx
#tailon --bind 127.0.0.1:18080 -r '/tailon/' -f /var/log/nginx/* &
#tailon --bind 0.0.0.0:18080 -r '/tailon/' -f /var/log/nginx/* &
python -m pytest /app