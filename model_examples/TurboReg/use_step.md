# 模型 TurboReg 使用步骤,python命令行版
TurboReg是一种高效且稳健的点云配准算法，支持CPU和GPU平台。该算法在保持领先水平的配准精度的同时，还能实现60帧每秒以上的处理速度。
## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118 http_proxy=http://2.2.2.122:8118
env | grep -i proxy
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
```
### 使用 git 克隆项目
git clone https://github.com/Laka-3DV/TurboReg.git
- 项目存储路径：/mnt/data2/zy_2025/github_store/TurboReg

### 环境配置
```bash
cd /mnt/data2/zy_2025/github_store/TurboReg
conda create -n turboreg python=3.11 -y
conda activate turboreg
pip install open3d tyro
#  Install PyTorch (select the appropriate version for your CUDA setup from https://pytorch.org/)
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
```

### 安装 TurboReg：
```bash
cd /mnt/data2/zy_2025/github_store/TurboReg/bindings
pip install .
cd ..
```

#### 安装 TurboReg 时报错
原因：gcc 版本过旧
```bash
# 查看版本
gcc --version
g++ --version

# 升级GCC
sudo apt update
sudo apt install gcc-10 g++-10
# 配置编译器默认版本
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100 --slave /usr/bin/g++ g++ /usr/bin/g++-10
```

#### 再次 安装 TurboReg：
```bash
cd /mnt/data2/zy_2025/github_store/TurboReg/bindings
pip install .
cd ..
```

## 运行项目演示文件
```bash
cd /mnt/data2/zy_2025/github_store/TurboReg/demo_py
python o3d_fpfh.py
```

## 创建文件使用 TurboReg 
```bash
touch run_my_ply_file.py
cp /home/zqdl_ai2060/zy_account/model_3d/model_examples/TurboReg/run_my_ply_file.py /mnt/data2/zy_2025/github_store/TurboReg/demo_py/

conda activate turboreg
cd /mnt/data2/zy_2025/github_store/TurboReg/demo_py

python run_my_ply_file.py
```
## 将结果传出到 122
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/TurboReg/out_trans_my D:\images\TurboReg



## docker 打包
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/TurboReg/docker /mnt/data2/zy_2025/github_store/TurboReg

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/TurboReg/docker
bash build_image.sh

# 5.运行容器
cd /mnt/data2/zy_2025/github_store/TurboReg/docker
bash run_container.sh

# 输出结果卷挂载：
# /mnt/data2/zy_2025/github_store/TurboReg/docker_demo_output:/model/TurboReg/docker_demo_output
# 查看输出结果图片：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/TurboReg/docker_demo_output
# 容器内部：
cd /model/TurboReg/docker_demo_output

```