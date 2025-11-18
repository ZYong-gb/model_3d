#!/bin/bash
# entrypoint.sh

# 如果任何一个命令执行失败（返回非零退出码），则立即退出
set -e 

echo "开始运行"

# 指向上级目录
DIR=$(pwd)
echo "当前路径: $DIR"

# model run
echo "模型开始推理"

conda run -n myenv python main.py --cfg ./config/test.yaml \
    SCENE scene0785_00/ \
    TEST.PATH ./data_store/example_data/ScanNet/ \
    LOGDIR ./checkpoints \
    LOADCKPT pretrained/model_000049.ckpt

echo "脚本执行完毕！"