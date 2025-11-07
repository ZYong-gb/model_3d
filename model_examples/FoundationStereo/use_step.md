# 模型 FoundationStereo 使用步骤,python命令行版
3d建模模型，最终输出为3d点云数据
## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118
export http_proxy=http://2.2.2.122:8118

```
### 使用 git 克隆项目
git clone https://github.com/NVlabs/FoundationStereo.git
- 项目存储路径：/mnt/data2/zy_2025/github_store/FoundationStereo


## 创建虚拟环境
```bash
conda env create -f environment.yml
conda run -n foundation_stereo pip install flash-attn
conda activate foundation_stereo
```

## 运行演示
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 将 https://drive.google.com/drive/folders/1VhPebc_mMxWKccrv7pdQLTvXYVcLYpsf 上下载的模型文件 pretrained_models 传到 FoundationStereo 项目中
scp -P 11202 -r D:\project_all\FoundationStereo\pretrained_models-20251013T044208Z-1-001\pretrained_models zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/FoundationStereo
### 开始运行项目
```bash
conda activate foundation_stereo
cd /mnt/data2/zy_2025/github_store/FoundationStereo/

# python scripts/run_demo.py --left_file ./assets/left.png --right_file ./assets/right.png --ckpt_dir ./pretrained_models/23-51-11/model_best_bp2.pth --out_dir ./test_outputs/
python scripts/run_demo.py --left_file ./assets/left.png --right_file ./assets/right.png --ckpt_dir ./pretrained_models/11-33-40/model_best_bp2.pth --out_dir ./test_outputs_1023/
```
### 将3d重建数据传到windows
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/FoundationStereo/test_outputs D:\images\output_image\



# 模型 FoundationStereo 使用步骤,docker 版
## 复制模型文件 FoundationStereo 到 model_3d/model_examples/FoundationStereo/docker 路径下
运行 bash cerate_ln.sh
## 构建 foundation_stereo 镜像
```bash
# 在 windows 系统pull镜像
# 将 21196d81f56b 镜像进行打包：
docker save -o 12.1.1-cudnn8-devel-ubuntu22.04.tar 21196d81f56b
# 将打包后的镜像 12.1.1-cudnn8-devel-ubuntu22.04.tar通过 scp 到2060：
scp -P 11202 -r D:\docker\docker_save\* zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/docker_images
# 在 Linux 加载打包后的镜像
cd /mnt/data2/zy_2025/docker_images
docker load -i 12.1.1-cudnn8-devel-ubuntu22.04.tar
# 给镜像打上标签
sudo docker tag d3262c91d05f nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04


#  进入目录 model_3d/model_examples/FoundationStereo/docker
cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/FoundationStereo/docker
# 构建镜像
sudo bash build_image.sh

# 启动容器：因为图像显示原因将在启动时运行文件将报错
sudo bash run_container.sh
# 在容器中激活环境 myenv
conda activate myenv
# 运行文件，开始推理
python scripts/run_demo.py --left_file ./assets/left.png --right_file ./assets/right.png --ckpt_dir ./pretrained_models/11-33-40/model_best_bp2.pth --out_dir ./docker_test_outputs/

```