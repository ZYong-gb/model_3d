#!/bin/bash

# 删除旧容器
docker rm -f depth_anything_3_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running depth_anything_3_container with GPU..."

docker run -it \
    --gpus all \
    --name depth_anything_3_container \
    --memory=32g \
    --memory-swap=64g \
    --shm-size=16g \
    -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets:/model/Depth-Anything-3/assets \
    -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace:/model/Depth-Anything-3/workspace \
    -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints:/model/Depth-Anything-3/checkpoints \
    -w /model/Depth-Anything-3 \
    --entrypoint /bin/bash \
    depth_anything_3:latest

# docker run -it \
#     --gpus all \
#     --name depth_anything_3_container \
#     -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets:/model/Depth-Anything-3/assets \
#     -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace:/model/Depth-Anything-3/workspace \
#     -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints:/model/Depth-Anything-3/checkpoints \
    # -w /model/Depth-Anything-3 \
#     depth_anything_3:latest