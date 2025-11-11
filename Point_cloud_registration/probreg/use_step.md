# probreg
- Probreg是一个用于实现基于概率模型的点云配准算法的库。
- CPD 配准
## run CPU_CPD
```bash
cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg
conda create -n probreg_ python=3.10 -y
conda activate probreg_
pip install cupy
pip install probreg
# one:
pip install open3d
python CPU_CPD.py
```

## run GPU_ICP
```bash
# 复制文件
cp -r /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs/* /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply

# 创建虚拟环境
cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/algothrim_registrion
conda create -n open3d_icp python=3.10 -y
conda activate open3d_icp
# 安装依赖包
pip install -r requirements.txt


# two:run
python GPU_ICP.py
# or
bash gpu_run.sh
# or
# generation and registration
bash all_run.sh
```
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply D:\images\配准结果\probreg


### 自动化流程---点云生成和配准
```bash
# 清空历史缓存：便于重零重新开始
cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg
bash clear_history.sh


# 开始自动流程
cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/code
conda activate open3d_icp

# 终端1：运行你的脚本
python auto_all_G_and_R.py

# 终端2：实时监控 full_scene.ply 大小和点数
watch -n 2 'head -5 ../output_ply/full_scene.ply | grep "element vertex"'
```


## run Rigid_CPD
```bash
cd /home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/algothrim_registrion
python Rigid_CPD.py

```

