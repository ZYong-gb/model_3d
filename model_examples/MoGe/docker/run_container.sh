#!/bin/bash

# 删除旧容器
docker rm -f moge_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running moge_container with GPU..."

# docker run -it \
#     --gpus all \
#     --name moge_container \
#     -v /mnt/data2/zy_2025/github_store/MoGe/docker_demo_output:/model/MoGe/docker_demo_output \
#     -v /mnt/data2/zy_2025/pretrained:/root/.cache/torch/hub/checkpoints
#     --entrypoint /bin/bash \
#     moge:latest

docker run -it \
    --gpus all \
    --name moge_container \
    -v /mnt/data2/zy_2025/github_store/MoGe/docker_demo_output:/model/MoGe/docker_demo_output \
    -v /mnt/data2/zy_2025/pretrained:/root/.cache/torch/hub/checkpoints \
    moge:latest \
    -i ./assets/杂物与输电线/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./docker_demo_output --maps --ply --glb