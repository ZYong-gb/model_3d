#!/bin/bash

# 删除旧容器
docker rm -f bridgedepth_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running bridgedepth_container with GPU..."

docker run -it \
    --gpus all \
    --name bridgedepth_container \
    -v "$DIR"/../docker_demo_output:/model/BridgeDepth/docker_demo_output \
    -v /mnt/data2/zy_2025/pretrained:/root/.cache/torch/hub/checkpoints \
    --entrypoint /bin/bash \
    bridgedepth:latest

# docker run -it \
#     --gpus all \
#     --name bridgedepth_container \
#     -v "$DIR"/../docker_demo_output:/model/BridgeDepth/docker_demo_output \
#     bridgedepth:latest