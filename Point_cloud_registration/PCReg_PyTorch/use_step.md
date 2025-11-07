# PCReg.PyTorch 使用
一种基于深度学习的简单点云配准流程。

## 环境准备
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118
export http_proxy=http://2.2.2.122:8118

# 进入项目存储路径
cd /mnt/data2/zy_2025/github_store
# 克隆项目
git clone https://github.com/zhulf0804/PCReg.PyTorch.git

# scp 模型到2060
scp -P 11202 -r D:\project_all\配准\PCReg_PyTorch\* zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/PCReg.PyTorch/ckpt_load


# 进入目录
cd /mnt/data2/zy_2025/github_store/PCReg.PyTorch
# 创建虚拟环境
conda create -n PCReg_PyTorch python=3.8 -y
conda activate PCReg_PyTorch

# 安装依赖包
pip install -r requirements.txt
pip install open3d==0.10.0.0

cd loss/cuda/emd_torch
python setup.py install
```
