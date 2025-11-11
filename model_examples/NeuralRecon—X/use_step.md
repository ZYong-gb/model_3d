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
pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

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


pip install -r requirements.txt

pip install git+https://github.com/mit-han-lab/torchsparse.git
```

### download checkpoint
```bash
cd /mnt/data2/zy_2025/github_store/NeuralRecon
mkdir checkpoints && cd checkpoints
# download
gdown --id 1zKuWqm9weHSm98SZKld1PbEddgLOQkQV
```

### run demo
```bash
# 将下载的数据传到 2060
scp -P 11202 -r D:\project_all\NeuraIRecon\neucon_demodata_b5f1 zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/NeuralRecon/demo_data/input_data

cd /mnt/data2/zy_2025/github_store/NeuralRecon
python demo.py --cfg ./config/demo.yaml
```




