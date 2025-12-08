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
docker pull pointcept/pointcept:v1.6.0-pytorch2.5.0-cuda12.4-cudnn9-devel
docker run --gpus all -it --rm pointcept/pointcept:v1.6.0-pytorch2.5.0-cuda12.4-cudnn9-devel bash
git clone https://github.com/facebookresearch/sonata
cd sonata
export PYTHONPATH=./ && python demo/0_pca.py
# Ignore the GUI error, we cannot expect a container to have its GUI, right?

```