# Pointcept
Pointcept是一个功能强大且灵活性极高的代码库，专门用于点云感知相关的研究。

## clone
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118 \
    http_proxy=http://2.2.2.122:8118

cd /mnt/data2/zy_2025/github_store
git clone https://github.com/Pointcept/Pointcept.git
```

## 通过官方 docker 使用 Pointcept
```bash
docker pull pointcept/pointcept:v1.5.0-pytorch2.0.1-cuda11.7-cudnn8-devel
docker run --gpus all -it --rm pointcept/pointcept:v1.5.0-pytorch2.0.1-cuda11.7-cudnn8-devel bash
git clone https://github.com/facebookresearch/sonata
cd sonata
pip install torch==2.4.1 \
    torchvision==0.19.1 \
    torchaudio==2.4.1 \
    scikit-image \
    omegaconf \
    opencv-contrib-python \
    imgaug \
    ninja \
    timm \
    albumentations \
    jupyterlab \
    scipy \
    joblib \
    scikit-learn \
    ruamel.yaml \
    trimesh \
    pyyaml \
    imageio \
    open3d \
    transformations \
    einops \
    gdown \
    nodejs \
    xformers==0.0.28.post1 \
    huggingface-hub

export PYTHONPATH=./ && python demo/0_pca.py
# Ignore the GUI error, we cannot expect a container to have its GUI, right?

```