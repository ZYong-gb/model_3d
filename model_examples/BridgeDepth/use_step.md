# 模型 BridgeDepth 使用步骤,python命令行版
BridgeDepth 将单目深度估计与立体深度估计相结合，通过左右两张双目图片，得到深度图，3d点云图和视差图
## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118 http_proxy=http://2.2.2.110:8118
env | grep -i proxy
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
```
### 使用 git 克隆项目
git clone https://github.com/aeolusguan/BridgeDepth
- 项目存储路径：/mnt/data2/zy_2025/github_store/BridgeDepth

### 环境配置
```bash
cd /mnt/data2/zy_2025/github_store/BridgeDepth
conda create -n bridgedepth python=3.10 -y
conda activate bridgedepth
pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu121

pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 检查依赖包安装结果
pip check
# --force-reinstall：强制重新安装缺失包
pip install --force-reinstall --no-cache-dir \
    pyparsing six \
    certifi idna urllib3 requests \
    pandas matplotlib seaborn \
    -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple


pip install opencv-python
pip install PyYAML
pip install yacs
pip install termcolor
pip install imageio
pip install tabulate
pip install einops timm fvcore
pip install omegaconf
```

### demo模型运行：输出结果为3D点云图以及深度图
```bash
# python demo.py --model_name rvc_pretrain  # also try with [rvc | eth3d_pretrain | middlebury_pretrain]
# If network issue, you can first download the checkpoint, and replace $checkpoint to the path of checkpoint file
# python demo.py --checkpoint_path $checkpoint
python demo.py --checkpoint_path ./checkpoints/bridge_rvc_pretrain.pth

# 将 demo_output 传到 windows 查看
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/BridgeDepth/demo_output D:\images\BridgeDepth\demo_output
```

### 运行项目，使用自己的图片
```bash
# 示例：
python infer.py --input $left_directory $right_directory --output $output_directory --from-pretrained rvc_pretrain # also try with [rvc | eth3d_pretrain | middlebury_pretrain]

# 分别创建文件夹 left_directory，right_directory，存储左右rgb图片
cd /mnt/data2/zy_2025/github_store/BridgeDepth/assets
mkdir input_images
cd input_images
mkdir left_images right_images
# 然后分别将 左右彩图存放在 left_images right_images 目录下

# 在命令行使用 mogrify 手动缩小输入图像
# mogrify -resize 512x384 ./assets/input_images/left_images/*.png -path ./assets/input_images/left_images_512x384/
# 复制 resize_images.py 文件到 /mnt/data2/zy_2025/github_store/BridgeDepth
cp /home/zqdl_ai2060/zy_account/model_3d/model_examples/BridgeDepth/resize_images.py /mnt/data2/zy_2025/github_store/BridgeDepth
# 运行 resize_images.py 文件对分辨率进行缩放
python resize_images.py


# 运行模型进行推理：输出结果为视差图
# 设置环境变量减少显存碎片
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
# 临时清理缓存
python -c "import torch; torch.cuda.empty_cache()"

# 法一：从 huggingface 在线下载模型
# python infer.py --input /mnt/data2/zy_2025/github_store/FoundationStereo/assets/left.png /mnt/data2/zy_2025/github_store/FoundationStereo/assets/right.png --output ./assets/out_images --from-pretrained rvc_pretrain

# 法二： 从本地路径通过名称加载模型 bridge_rvc_pretrain.pth
python infer.py --input ./assets/input_images/left_images_512x384// ./assets/input_images/right_images_512x384/ --output ./assets/out_images --from-pretrained ./checkpoints/bridge_rvc_pretrain.pth
```
