#!/bin/bash

# 删除旧容器
docker rm -f depth_anything_v2_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running depth_anything_v2_container with GPU..."

# docker run -it \
#     --gpus all \
#     --name depth_anything_v2_container \
#     -v "$DIR"/../docker_demo_output:/model/Depth-Anything-V2/docker_demo_output \
#     --entrypoint /bin/bash \
#     depth_anything_v2:latest

docker run -it \
    --gpus all \
    --name depth_anything_v2_container \
    -v "$DIR"/../docker_demo_output:/model/Depth-Anything-V2/docker_demo_output \
    -v /mnt/data2/zy_2025/pretrained:/root/.cache/torch/hub/checkpoints \
    depth_anything_v2:latest