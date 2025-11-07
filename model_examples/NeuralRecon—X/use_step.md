# 模型 NeuralRecon 使用步骤

## 设置代理
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118
export http_proxy=http://2.2.2.122:8118
```

## 模型下载
### 进入目录
cd /mnt/data2/zy_2025/github_store/
### 从 github 下载模型
git clone https://github.com/zju3dv/NeuralRecon.git

## 环境准备
### 创建环境（指定Python版本）
```bash
conda create -n neucon python=3.10 -y
conda activate neucon
```
### 安装PyTorch及依赖
<!-- conda install pytorch=1.6.0 torchvision=0.7.0 cudatoolkit=10.2 -c pytorch -->
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
### 安装其他依赖
```bash
# 进入 /mnt/data2/zy_2025/github_store/NeuralRecon
cd /mnt/data2/zy_2025/github_store/NeuralRecon

pip install ipython
pip install tqdm
pip install numba

# 清除代理再安装
unset https_proxy http_proxy
conda install -c conda-forge sparsehash
```
### 安装 requirements 中的依赖
pip install -r requirements.txt
#### 解决错误
- ERROR: Failed building wheel for pycuda
- ERROR: Could not build wheels for pycuda, which is required to install pyproject.toml-based projects
```bash

```
### 继续安装 requirements.txt 中的依赖包
```bash
pip install tensorboardX
pip install scikit-image
pip install trimesh~=3.9.18
pip install yacs
pip install h5py
pip install loguru
pip install gdown
pip install pyrender~=0.1.45
pip install pyglet
pip install open3d
```


pip install git+https://github.com/mit-han-lab/torchsparse.git

