# 项目 Depth Anything 3
- 它能从任意视觉输入中预测出具有空间一致性的几何结构，无论是否已知相机的姿态信息，并且支持多视图深度估计与姿态估计
- 生成深度图以及使用多视图RGB和深度图生成融合后的3d点云数据，（官方仅提供单卡推理实现）

## Virtual env 中使用
### clone
```bash
# 在命令行依次输入以下代码，即可配置代理
export https_proxy=http://2.2.2.110:8118 http_proxy=http://2.2.2.110:8118
export https_proxy=http://2.2.2.122:8118 http_proxy=http://2.2.2.122:8118

cd /mnt/data2/zy_2025/github_store
git clone https://github.com/ByteDance-Seed/Depth-Anything-3.git

```

### 环境配置
#### 进入项目文件 Depth-Anything-3
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3
#### 创建虚拟环境
```bash
conda create -n Depth-Anything-3 python=3.10 -y
conda activate Depth-Anything-3
```
#### 安装依赖包
```bash
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install xformers 
pip install -r requirements.txt

pip install -e .
pip install --no-build-isolation git+https://github.com/nerfstudio-project/gsplat.git@0b4dddf04cb687367602c01196913cde6a743d70
pip install -e ".[app]"
pip install -e ".[all]"
```
#### 文件传输
```bash
# checkpoints 传输
scp -P 11202 -r D:\project_all\Depth-Anything-3\checkpoints\ zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-3


```

### model use
#### way 1:
```bash
# 进入路径
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3
conda activate Depth-Anything-3

# 设置环境变量强制离线模式 加载模型
# transformers 库不联网
export TRANSFORMERS_OFFLINE=1
# datasets 库不联网
export HF_DATASETS_OFFLINE=1
# 所有 Hugging Face 相关操作强制离线（最彻底）
export HF_HUB_OFFLINE=1

# 设置环境变量
# 设置本地模型存储路径
export MODEL_DIR=/mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints/DA3NESTED-GIANT-LARGE/
# 设置输出目录
export GALLERY_DIR=workspace/gallery
mkdir -p $GALLERY_DIR

# 开始推理
da3 auto assets/examples/SOH \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/examples/SOH \
    --model-dir ${MODEL_DIR}

# 查看相关参数
da3 auto --help
da3 video --help

# scp
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace D:\images\Depth-Anything-3\workspace

```

### way 2: --use-backend 参数必须开两个终端cli
```bash
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3
conda activate Depth-Anything-3

export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export HF_HUB_OFFLINE=1


# export MODEL_DIR=depth-anything/DA3NESTED-GIANT-LARGE
export MODEL_DIR=/mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints/DA3NESTED-GIANT-LARGE/
# This can be a Hugging Face repository or a local directory
# If you encounter network issues, consider using the following mirror: export HF_ENDPOINT=https://hf-mirror.com
# Alternatively, you can download the model directly from Hugging Face
export GALLERY_DIR=workspace/gallery
mkdir -p $GALLERY_DIR

# CLI auto mode with backend reuse
# 终端命令行1，运行：
da3 backend --model-dir ${MODEL_DIR} --gallery-dir ${GALLERY_DIR} 

# 再开一个终端命令行2，运行：
# 图片
da3 auto assets/examples/SOH \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/TEST_BACKEND/SOH \
    --model-dir ${MODEL_DIR} \
    --use-backend
# 视频
# CLI video processing with feature visualization
da3 video assets/examples/robot_unitree.mp4 \
    --fps 1200 \
    --export-dir ${GALLERY_DIR}/TEST_BACKEND/robo \
    --model-dir ${MODEL_DIR} \
    --export-format glb-feat_vis \
    --feat-vis-fps 15 \
    --process-res-method lower_bound_resize \
    --export-feat "11,21,31" \
    --process-res 378 \
    --use-backend 

# 查看相关参数
da3 video --help

# CLI auto mode without backend reuse
da3 auto assets/examples/SOH \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/TEST_CLI/SOH \
    --model-dir ${MODEL_DIR}
```
### use way 3:
```bash
cp -r /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace/gallery/TEST_BACKEND/robo/input_images/* /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/video_rot_to_photo
for i in {6..999}; do rm -f $(printf "%06d.png" $i) 2>/dev/null; done
# 图片
da3 auto /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/video_rot_to_photo \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/examples/video_rot_to_photo \
    --model-dir ${MODEL_DIR} \
    --use-backend



mkdir -p -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/PLDM_images/aug_data0_0_0/
cp -r /mnt/data2/zy_2025/github_store/MoGe/assets/PLDM_images/aug_data0_0_0/* /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/PLDM_images/aug_data0_0_0/
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/PLDM_images/aug_data0_0_0/
rm -f {7..999}.jpg
# 图片
da3 auto /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/PLDM_images/aug_data0_0_0 \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/examples/PLDM_images/ \
    --model-dir ${MODEL_DIR} \
    --auto-cleanup \
    --use-backend


mkdir -p -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/zqdl_shinei/
cp -r /mnt/data2/zy_2025/github_store/MoGe/assets/zqdl_shinei/*.jpg /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/zqdl_shinei/
# 图片
da3 auto /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets/examples/zqdl_shinei \
    --export-format glb-npz-ply-3DGS \
    --export-dir ${GALLERY_DIR}/examples/zqdl_shinei/ \
    --model-dir ${MODEL_DIR} \
    --auto-cleanup \
    --use-backend

scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace D:\images\Depth-Anything-3\workspace

```


# docker 打包
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/Depth-Anything-3/docker /mnt/data2/zy_2025/github_store/Depth-Anything-3

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/docker
bash build_image.sh

# 5.运行容器
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/docker
bash run_container.sh

# 容器内部运行：
cd /model/Depth-Anything-3
conda activate myenv

# 设置环境变量强制离线模式 加载模型
# transformers 库不联网
export TRANSFORMERS_OFFLINE=1
# datasets 库不联网
export HF_DATASETS_OFFLINE=1
# 所有 Hugging Face 相关操作强制离线（最彻底）
export HF_HUB_OFFLINE=1

# 设置环境变量
# 设置本地模型存储路径
export MODEL_DIR=/model/Depth-Anything-3/checkpoints/DA3NESTED-GIANT-LARGE/
# 设置输出目录
export GALLERY_DIR=workspace/gallery
mkdir -p $GALLERY_DIR

# 开始推理1
da3 auto assets/examples/SOH \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/examples/SOH \
    --model-dir ${MODEL_DIR}

# 开始推理2
da3 auto assets/examples/zqdl_shinei \
    --export-format glb-npz \
    --export-dir ${GALLERY_DIR}/examples/zqdl_shinei/ \
    --model-dir ${MODEL_DIR} \
    --device cuda:1 \
    --auto-cleanup

# --device 参数: cpu, cuda, ipu, xpu, mkldnn, opengl, opencl, ideep, hip, ve, fpga, ort, xla, lazy, vulkan, mps, meta, hpu, mtia ,无实现多卡代码


# 输出结果卷挂载：
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets:/model/Depth-Anything-3/assets \
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace:/model/Depth-Anything-3/workspace \
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints:/model/Depth-Anything-3/checkpoints \
# 查看图片，宿主机：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace
# 查看图片，容器中：
cd /model/Depth-Anything-3/workspace
```