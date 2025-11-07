#!bin/bash
set -x  # 启用命令跟踪（调试模式）

cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/code
python move_and_run_one_image.py

cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg
python GPU_ICP.py