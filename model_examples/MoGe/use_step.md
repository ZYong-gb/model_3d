# 模型 MoGe 使用步骤,python命令行版
3d点云图，最终输出为rgb图像的点云图
## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118 http_proxy=http://2.2.2.110:8118
```
### 使用 git 克隆项目
git clone https://github.com/microsoft/MoGe.git
- 项目存储路径：/mnt/data2/zy_2025/github_store/MoGe

## 环境配置
### 进入项目文件 Depth-Anything-V2
cd /mnt/data2/zy_2025/github_store/MoGe
### 创建虚拟环境
```bash
conda create -n MoGe python=3.10 -y
conda activate MoGe
```
### 安装依赖包
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

#### 下载 依赖项目 utils3d 
```bash
cd /mnt/data2/zy_2025/github_store/MoGe
#### 下载 依赖项目 utils3d 到 /mnt/data2/zy_2025/github_store/MoGe 路径下
git clone https://github.com/EasternJournalist/utils3d.git
# utils3d 的存储路径为：/mnt/data2/zy_2025/github_store/MoGe/utils3d

### 安装 utils3d
cd /mnt/data2/zy_2025/github_store/MoGe
pip install ./utils3d
```
### 安装依赖包
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install filelock
### 安装 cv2
- pip install opencv-python
- Successfully installed opencv-python-4.12.0.88

### 降级 PyTorch 到支持 CUDA 12.1（2060的安装版本） 的版本
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121

### 下载模型训练参数文件 checkpoints
- hunggingface 下载 moge-2-vitl-normal，并传到 2060
- scp -P 11202 -r D:\project_all\MoGe\checkpoints\moge-2-vitl-normal zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/Ruicheng

- scp -P 11202 -r D:\images\MoGe\cut_pic zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets
- scp -P 11202 -r D:\project_all\photo2D_to_3D_point_cloud\photo_RGB_D\PLDM_images\ zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets
- scp -P 11202 -r D:\images\杂物与输电线\ zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets

### 复制模型运行文件 model_use.py 到 /mnt/data2/zy_2025/github_store/MoGe 路径下
cp /home/zqdl_ai2060/zy_account/model_3d/model_examples/MoGe/model_use.py /mnt/data2/zy_2025/github_store/MoGe

### 模型运行
```bash
# cd /mnt/data2/zy_2025/github_store/MoGe
# pip install --upgrade utils3d
# python model_use.py
```

### 安装依赖包
```bash
cd /mnt/data2/zy_2025/github_store/MoGe

pip check
pip install packaging requests python-dateutil tzdata matplotlib

# cd /mnt/data2/zy_2025/github_store/MoGe
pip install -e .

```

### 模型运行
```bash
cd /mnt/data2/zy_2025/github_store/MoGe
conda activate MoGe


# Save the output [maps], [glb] and [ply] files
# moge infer -i IMAGES_FOLDER_OR_IMAGE_PATH --o OUTPUT_FOLDER --maps --glb --ply
moge infer -i ./assets/pic/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/pic/output_images --maps --ply --glb
moge infer -i ./assets/zqdl_shinei/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/zqdl_shinei/output_images --maps --ply --glb
moge infer -i ./assets/keywords/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/keywords/output_images --maps --ply --glb
moge infer -i ./assets/cut_pic/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/cut_pic/output_images --maps --ply --glb
moge infer -i ./assets/PLDM_images/aug_data0_0_0/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/PLDM_images/output_images --maps --ply --glb
moge infer -i ./assets/杂物与输电线/ --pretrained ./Ruicheng/moge-2-vitl-normal/model.pt -o ./assets/杂物与输电线/output_images --maps --ply --glb

# Show the result in a window (requires pyglet < 2.0, e.g. pip install pyglet==1.5.29)
# moge infer -i IMAGES_FOLDER_OR_IMAGE_PATH --o OUTPUT_FOLDER --show
```

### 运行结果 scp
```bash
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets/keywords D:\images\MoGe
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets/cut_pic D:\images\MoGe
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets/PLDM_images D:\images\MoGe
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/MoGe/assets/杂物与输电线 D:\images\MoGe
```


## docker 打包
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/MoGe/docker /mnt/data2/zy_2025/github_store/MoGe

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/MoGe/docker
bash build_image.sh

# 5.运行容器
cd /mnt/data2/zy_2025/github_store/MoGe/docker
bash run_container.sh

# 输出结果卷挂载：
# /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output:/model/Depth-Anything-V2/docker_demo_output
# 查看图片：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output
cd /model/Depth-Anything-V2/docker_demo_output
```