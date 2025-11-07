#!/bin/bash

# 删除旧容器
docker rm -f foundation_stereo_container 2>/dev/null || true

# 指向上级目录
# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running FoundationStereo with GPU..."

# # 直接运行文件将报错
# docker run \
#     --gpus all \
#     --name foundation_stereo_container \
#     -v "$DIR"/FoundationStereo/assets:/model/FoundationStereo/assets \
#     -v "$DIR"/FoundationStereo/docker_test_outputs:/model/FoundationStereo/docker_test_outputs \
#     -w /model/FoundationStereo \
#     foundationstereo:latest \
#     --left_file assets/left.png \
#     --right_file assets/right.png \
#     --ckpt_dir pretrained_models/11-33-40/model_best_bp2.pth \
#     --out_dir docker_test_outputs


docker run -it \
    --gpus all \
    --name foundation_stereo_container \
    -v "$DIR"/FoundationStereo/assets:/model/FoundationStereo/assets \
    -v "$DIR"/FoundationStereo/docker_test_outputs:/model/FoundationStereo/docker_test_outputs \
    -w /model/FoundationStereo \
    --entrypoint /bin/bash \
    foundationstereo:latest