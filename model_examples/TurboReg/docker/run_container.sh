#!/bin/bash

# 删除旧容器
docker rm -f turboreg_container 2>/dev/null || true

# 指向上级目录
DIR=$(pwd)
# 或者
# DIR=/home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo
echo "DIR: $DIR"
echo "Running turboreg_container with GPU..."

# docker run -it \
#     --gpus all \
#     --name turboreg_container \
#     -v "$DIR"/../demo_data://model/TurboReg/demo_data \      # 输入挂载 
#     -v "$DIR"/../docker_demo_output:/model/TurboReg/out_trans_my \  # 输出挂载
#     --entrypoint /bin/bash \
#     turboreg:latest

docker run -it \
    --gpus all \
    --name turboreg_container \
    -v "$DIR"/../demo_data:/model/TurboReg/demo_data \
    -v "$DIR"/../docker_demo_output:/model/TurboReg/out_trans_my \
    -w /model/TurboReg/demo_py \
    turboreg:latest