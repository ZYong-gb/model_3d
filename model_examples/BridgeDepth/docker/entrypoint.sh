#!/bin/bash
# entrypoint.sh

# 如果任何一个命令执行失败（返回非零退出码），则立即退出
set -e 

echo "开始运行"

# 运行尺寸裁剪脚本
echo "运行尺寸裁剪脚本"
conda run -n myenv python resize_images.py

# 注意：PYTORCH_CUDA_ALLOC_CONF 环境变量已在 Dockerfile 中设置，在脚本内再次 export 也可以，但通常在 Dockerfile 设置更早生效。
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# 临时清理缓存 (也应在 myenv 环境中运行)
echo "clear cache temp"
conda run -n myenv python -c "import torch; torch.cuda.empty_cache()"

# 指向上级目录
DIR=$(pwd)
echo "当前路径: $DIR"

# model run
echo "模型开始推理"

conda run -n myenv python infer.py --input ./assets/input_images/left_images_512x384/ ./assets/input_images/right_images_512x384/ --output ./docker_demo_output --from-pretrained ./checkpoints/bridge_rvc_pretrain.pth

echo "所有脚本执行完毕！"