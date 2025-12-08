# OpenPCDet
3d 物体检测算法，专门用于基于激光雷达的3D物体检测。


## 克隆 github 上的仓库
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118 \
    http_proxy=http://2.2.2.110:8118

cd /mnt/data2/zy_2025/github_store
git clone https://github.com/open-mmlab/OpenPCDet.git
```

## 环境配置
```bash
cd /mnt/data2/zy_2025/github_store/OpenPCDet

conda create -n OpenPCDet python=3.10 -y
conda activate OpenPCDet
```
## 依赖安装
###  spconv 安装
```bash
cd /mnt/data2/zy_2025/github_store/OpenPCDet
git clone https://github.com/FindDefinition/cumm.git
cd ./cumm
pip install -e .


git clone https://github.com/traveller59/spconv.git
cd ./spconv
pip install -e .
```