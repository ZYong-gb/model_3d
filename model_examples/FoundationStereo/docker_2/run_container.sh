#!/bin/bash

# 删除旧容器
docker rm -f foundation_stereo_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running foundation_stereo_container with GPU..."

# docker run -it \
#     --gpus all \
#     --name foundation_stereo_container \
#     -v /mnt/data2/zy_2025/github_store/FoundationStereo/assets:/model/FoundationStereo/assets \
#     -v /mnt/data2/zy_2025/github_store/FoundationStereo/docker_demo_output:/model/FoundationStereo/docker_demo_output \
#     --entrypoint /bin/bash \
#     foundationstereo:latest

docker run -it \
    --gpus all \
    --name foundation_stereo_container \
    -v /mnt/data2/zy_2025/github_store/FoundationStereo/scripts:/model/FoundationStereo/scripts \
    -v /mnt/data2/zy_2025/github_store/FoundationStereo/assets:/model/FoundationStereo/assets \
    -v /mnt/data2/zy_2025/github_store/FoundationStereo/docker_demo_output:/model/FoundationStereo/docker_demo_output \
    foundationstereo:latest \
    python scripts/run_demo.py \
    --left_file assets/left.png \
    --right_file assets/right.png \
    --ckpt_dir pretrained_models/11-33-40/model_best_bp2.pth \
    --out_dir docker_demo_output