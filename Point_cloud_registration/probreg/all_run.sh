#!/bin/bash
set -x  # 启用命令跟踪（调试模式）

cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main
bash run.sh

cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg
bash gpu_run.sh