#!/bin/bash

python3 /testing/test_http_server.py &
locust -f /testing/locustfile.py --host=http://nginx