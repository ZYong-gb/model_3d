# 项目 TripoSR 使用步骤

## 设置代理
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118
export http_proxy=http://2.2.2.110:8118
```

## 模型下载
### 进入目录
cd /mnt/data2/zy_2025/github_store/
### 从 github 下载模型
git clone https://github.com/VAST-AI-Research/TripoSR.git

## 环境配置
### 创建环境（指定Python版本）
- conda create -n TripoSR python=3.10 -y
- conda activate TripoSR

### 安装  requirements.txt 中的依赖
```bash
cd /mnt/data2/zy_2025/github_store/TripoSR
pip install --upgrade setuptools
pip install -r requirements.txt
```
#### 解决 torchmcubes 安装错误
1. 法一：尝试自动安装
```bash
sudo apt update
sudo apt install cmake build-essential g++ ninja-build
pip install --upgrade pip setuptools wheel
# 清理 pip 缓存
pip cache purge
# 或者强制重新安装，不使用缓存
pip install -r requirements.txt
```
2. 法二：尝试手动安装
```bash
# 克隆源码
git clone https://github.com/tatsy/torchmcubes.git
cd torchmcubes
# 手动安装
pip install -e .
```
## 环境配置失败