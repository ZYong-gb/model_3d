# VisFusion
一种基于视频的、具有可见性感知功能的在线3D场景重建技术

## clone
```bash
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/huiyu-gao/VisFusion.git
```

## install
```bash
cd /mnt/data2/zy_2025/github_store/VisFusion

sudo apt install libsparsehash-dev
conda create -n visfusion python=3.9 -y
conda activate visfusion

pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116
pip install ipython
conda install sparsehash -y

export https_proxy=http://2.2.2.122:8118 http_proxy=http://2.2.2.122:8118

pip install ray transforms3d tqdm opencv-python numba tensorboardX scikit-image trimesh yacs h5py loguru
pip install pyrender pyglet open3d

# correct 指定cuda的版本为11.3
export PATH=/usr/local/cuda-11.3/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.3/lib64:$LD_LIBRARY_PATH

# 用 GCC 9 编译安装 torchsparse==1.4.0
CC=gcc-9 CXX=g++-9 pip install git+https://github.com/mit-han-lab/torchsparse.git@v1.4.0

# 降级版本
pip install "numpy>=1.20,<2"
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-python==4.8.1.78
pip uninstall scikit-image -y
pip install scikit-image==0.22.0
# 升级版本
pip install --upgrade "scikit-image>=0.20.0"

# 修改代码：将 single_mesh=single_layer_mesh 代码注释掉：
# @staticmethod
# def tsdf2mesh(voxel_size, origin, tsdf_vol, layer, single_layer_mesh):
#     verts, faces, norms, vals = measure.marching_cubes(tsdf_vol, level=0, allow_degenerate=False)
#                                                         # ,single_mesh=single_layer_mesh)
```

## data prepare
```bash
cd /mnt/data2/zy_2025/github_store/VisFusion
mkdir data_store
cd /mnt/data2/zy_2025/github_store/VisFusion/data_store
scp -P 11202 -r D:\project_all\VisFusion\example_data zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/VisFusion/data_store
```

## run demo
```bash
cd /mnt/data2/zy_2025/github_store/VisFusion
conda activate visfusion


python main.py --cfg ./config/test.yaml \
                SCENE scene0785_00/ \
                TEST.PATH ./data_store/example_data/ScanNet/ \
                LOGDIR ./checkpoints \
                LOADCKPT pretrained/model_000049.ckpt


# 输出路径：/mnt/data2/zy_2025/github_store/VisFusion/results/scene_scannet_checkpoints_fusion_eval_49
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/VisFusion/results/scene_scannet_checkpoints_fusion_eval_49 D:\images\VisFusion


# python main.py --cfg ./config/test.yaml \
#                 SCENE scene0785_00 \ 
#                 TEST.PATH ./data_store/example_data/ScanNet/ \
#                 LOGDIR: ./checkpoints \ 
#                 LOADCKPT pretrained/model_000049.ckpt \ 
#                 MODEL.SINGLE_LAYER_MESH True
```

# 使用 docker 进行打包
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/VisFusion/docker /mnt/data2/zy_2025/github_store/VisFusion

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/VisFusion/docker
bash build_image.sh

# 5.运行容器
cd /mnt/data2/zy_2025/github_store/VisFusion/docker
bash run_container.sh

# 输入卷挂载：
# /mnt/data2/zy_2025/github_store/VisFusion/data_store/example_data/:/model/VisFusion/data_store/example_data  
# 输出卷挂载：
# /mnt/data2/zy_2025/github_store/VisFusion/results:/model/VisFusion/results 

# 查看输出结果图片：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/VisFusion/results
# 容器内部：
cd /model/TurboReg/docker_demo_output
```