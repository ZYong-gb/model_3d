#!/bin/bash

# 删除旧容器
docker rm -f adelaidepth_main_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running adelaidepth_main_container with GPU..."

docker run -it \
    --gpus all \
    --name adelaidepth_main_container \
    -v "$DIR"/Minist_Test/test_images:/model/Minist_Test/test_images \
    -w /model/AdelaiDepth-main/LeReS/Minist_Test \
    --entrypoint /bin/bash \
    adelaidepth_main:latest \




