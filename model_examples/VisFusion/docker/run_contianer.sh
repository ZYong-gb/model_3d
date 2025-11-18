#!/bin/bash

# 删除旧容器
docker rm -f visfusion_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running visfusion_container with GPU..."

# docker run -it \
#     --gpus all \
#     --name visfusion_container \
#     -v "$DIR"/../data_store/example_data/:/model/VisFusion/data_store/example_data \
#     -v "$DIR"/../results:/model/VisFusion/results \
#     --entrypoint /bin/bash \
#     visfusion:latest

docker run -it \
    --gpus all \
    --name visfusion_container \
    -v "$DIR"/../data_store/example_data/:/model/VisFusion/data_store/example_data \
    -v "$DIR"/../results:/model/VisFusion/results \
    visfusion:latest