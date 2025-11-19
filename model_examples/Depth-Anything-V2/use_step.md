# 模型 Depth-Anything-V2 使用步骤,python命令行版
深度图，最终输出为rgb图像的深度图
## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118
export http_proxy=http://2.2.2.110:8118
```
### 使用 git 克隆项目
git clone https://github.com/DepthAnything/Depth-Anything-V2.git
- 项目存储路径：/mnt/data2/zy_2025/github_store/Depth-Anything-V2

## 环境配置
### 进入项目文件 Depth-Anything-V2
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main
### 创建虚拟环境
```bash
conda create -n Depth-Anything-V2-main python=3.10 -y
conda activate Depth-Anything-V2-main
```
### 安装依赖包
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

### 降级 PyTorch 到支持 CUDA 12.1（2060的安装版本） 的版本
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121

### 下载 checkpoints 文件到 D:\project_all\Depth-Anything-V2-main\Depth-Anything-V2-main\checkpoints
https://github.com/DepthAnything/Depth-Anything-V2.git
### 将 checkpoints 文件保存到 github_store/Depth-Anything-V2-main 路径下
scp -P 11202 -r D:\project_all\Depth-Anything-V2-main\Depth-Anything-V2-main\checkpoints zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-V2-main

### 将文件 model_3d/model_examples/Depth-Anything-V2/model_use.py 复制到路径 /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main 下
cp /home/zqdl_ai2060/zy_account/model_3d/model_examples/Depth-Anything-V2/model_use.py /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main

### 运行 model_use.py 或 run.py 文件:图片生成深度图
```bash
conda activate Depth-Anything-V2-main
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main

# cp photo
cp /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/test_images/*.jpg /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/assets/examples/zqdl_shinei
cp /mnt/data2/zy_2025/github_store/MoGe/assets/full_scene/PANO_20251119_120902.jpg /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/assets/examples/full_scene

# run photo to dept
python model_use.py

# or
# python run.py \
#   --encoder <vits | vitb | vitl | vitg> \
#   --img-path <path> --outdir <outdir> \
#   [--input-size <size>] [--pred-only] [--grayscale]

python run.py --encoder vitl --img-path assets/examples/demo01.jpg --outdir assets/out_images
python run.py --encoder vitl --img-path assets/examples --outdir assets/out_images

# 测试 输电线图片
cp -r /home/zqdl_ai2060/zy_account/model_3d/images/pic /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/assets
python run.py --encoder vitl --img-path assets/pic --outdir assets/pic_dept

python run.py --encoder vitl --img-path assets/examples/full_scene --outdir assets/examples/full_scene/output

```
### 视频生成深度图
```bash
python run_video.py \
  --encoder <vits | vitb | vitl | vitg> \
  --video-path assets/examples_video --outdir video_depth_vis \
  [--input-size <size>] [--pred-only] [--grayscale]

python run_video.py --encoder vitl --video-path assets/examples_video --outdir assets/video_depth_vis
  ```

### 将结果图传到 windows 系统查看
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/assets D:\images\Depth-Anything-V2
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/assets/examples/full_scene/output D:\images\Depth-Anything-V2\assets\full_scene


## docker 打包
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/Depth-Anything-V2/docker /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker
bash build_image.sh

# 5.运行容器
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker
bash run_container.sh

# 输出结果卷挂载：
# /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output:/model/Depth-Anything-V2/docker_demo_output
# 查看图片：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output
cd /model/Depth-Anything-V2/docker_demo_output
```