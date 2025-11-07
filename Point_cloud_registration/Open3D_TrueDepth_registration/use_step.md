
# Open3D_TrueDepth_registration 项目
点云配准：这个演示展示了如何将 iPhone 的 TrueDepth 相机用作 3D 扫描仪。该工具能够自动完成 3D 点云的配准处理，并且还可以选择生成带有颜色的 3D 网格模型。在测试中，用户需要围绕某个物体进行 360 度的旋转拍摄，每旋转大约 10 度就记录一次数据。

## 下载测试数据集
```bash
# 下载项目 Open3D_TrueDepth_registration 代码 
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/nghiaho12/Open3D_TrueDepth_registration.git

# 下载测试数据集
cd /mnt/data2/zy_2025/github_store/Open3D_TrueDepth_registration
curl -O https://nghiaho.com/uploads/box_can.zip
# 解压文件
unzip box_can.zip

# 创建并激活虚拟环境
conda create -n Open3D_TrueDepth_registration python=3.10 -y
conda activate Open3D_TrueDepth_registration

# 安装 pybind11 子模块
git submodule update --init --recursive

# 安装依赖包
pip install open3d
pip install numpy
pip install scipy
pip install opencv-python
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install scikit-learn
pip install pandas

# 安装以下 C++ 库
sudo apt-get install libeigen3-dev
sudo apt-get install libceres-dev

# 进入目录：
cd /mnt/data2/zy_2025/github_store/Open3D_TrueDepth_registration/cpp
mkdir build
cd /mnt/data2/zy_2025/github_store/Open3D_TrueDepth_registration/cpp/build
cmake ..


```
