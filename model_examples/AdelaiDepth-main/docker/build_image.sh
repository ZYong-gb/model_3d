#!bin/bash

sudo docker build \
    --build-arg HTTP_PROXY=http://2.2.2.122:8118 \
    --build-arg HTTPS_PROXY=http://2.2.2.122:8118 \
    --build-arg http_proxy=http://2.2.2.122:8118 \
    --build-arg https_proxy=http://2.2.2.122:8118 \
    -t adelaidepth_main:latest .