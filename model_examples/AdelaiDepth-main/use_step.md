# 项目: aim-uofa/AdelaiDepth
## 测试: Best Paper Finalist:Learning to Recover 3D Scene Shape from a Single Image 项目
https://github.com/aim-uofa/AdelaiDepth/tree/main/LeReS
1. 将项目 AdelaiDepth 克隆在本地：
git clone git@github.com:aim-uofa/AdelaiDepth.git
2. 创建虚拟环境并安装包：
```bash
cd LeReS
conda create -n LeReS python=3.8 -y
conda activate LeRes
conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
# 进入 /AdelaiDepth-main/LeReS
pip install -r requirements.txt
```
3. 继续安装包：
sudo apt-get install libsparsehash-dev
4. 克隆项目 mit-han-lab/torchsparse 的v1.2.0版本 到 LeReS路径下：
git clone -b v1.2.0 git@github.com:mit-han-lab/torchsparse.git

- 注意：可能无法直接 clone 该项目：
可以通过项目网址：https://github.com/mit-han-lab/torchsparse/tree/v1.2.0 直接下载 .zip 压缩包，解压之后，将下载的文件目录 torchsparse-1.2.0 通过scp传进2060服务器：
将 torchsparse-1.2.0 文件夹传到文件夹路径：AdelaiDepth-main/LeReS 下
- 然后进入 AdelaiDepth-main/LeReS/torchsparse-1.2.0 进行安装：
cd torchsparse-1.2.0
pip install -e .

- 重新安装 numpy==1.23.5 版本
pip install numpy==1.23.5 

5. 数据准备
- 1. 在 AdelaiDepth-main/LeReS/Minist_Test/test_images 路径下保存用来生成3d点云图像的原始RGB图片
- 2. 在 AdelaiDepth-main/LeReS/Minist_Test/test_images 路径下创建 outputs 文件夹，用来存放生成的3d点云 ply 图像
```bash
# 文件传入
scp -P 11202 -r D:\project_all\双目摄像机\saved_frames\* zqdl_ai2060@183.221.0.158:/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/test_images
scp -P 11202 -r D:\images\AdelaiDepth_outputs\input_images\* zqdl_ai2060@183.221.0.158:/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/test_images
# 文件传出
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/test_images D:\images\AdelaiDepth_outputs\

```
6. 开始运行代码 steps1：
- 进入 AdelaiDepth-main/LeReS/Minist_Test 文件夹：
<!-- cd /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test -->
cd /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test

- 添加 Minist_Test 的路径到环境变量 PYTHONPATH：
<!-- export PYTHONPATH="/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test" -->
export PYTHONPATH="/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test"
conda activate LeRes

7. 开始运行代码 steps2：
- 1. 使用 ResNet50 backbone 框架生成3d图
    - 生成深度图：python ./tools/test_depth.py --load_ckpt res50.pth --backbone resnet50
    - 生成3d点云图：python ./tools/test_shape.py --load_ckpt res50.pth --backbone resnet50
- 2. 使用 ResNeXt101 backbone 框架生成3d图
    - 生成深度图：python ./tools/test_depth.py --load_ckpt res101.pth --backbone resnext101
    - 生成3d点云图：python ./tools/test_shape.py --load_ckpt res101.pth --backbone resnext101
- 3. 直接运行：
    - cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main
    - bash run.sh



## docker 打包 1
### 复制项目文件 requirements.txt 到 model_3d/model_examples/AdelaiDepth-main/docker 路径
```bash
# cp /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/requirements.txt /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/docker
# cp -r /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/torchsparse-1.2.0 /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/docker
# cp -r /home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/docker

cp -r /home/zqdl_ai2060/zy_account/AdelaiDepth-main /mnt/data2/zy_2025/github_store
```
### 移动 docker 文件夹到/mnt
mv /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/docker /mnt/data2/zy_2025/github_store/AdelaiDepth


### 构建并运行
```bash
#  进入目录 model_3d/model_examples/FoundationStereo/docker
cd /mnt/data2/zy_2025/github_store/AdelaiDepth/docker

# 构建镜像
sudo bash build_image.sh

# 启动容器
sudo bash run_container.sh

# 在容器中激活环境 myenv
conda activate myenv

# 安装依赖
cd /model/AdelaiDepth-main/LeReS/torchsparse-1.2.0
pip install -e .

# 运行文件，开始推理
cd /model/AdelaiDepth-main/LeReS/Minist_Test
# 使用 ResNet50 backbone 框架生成3d图
# 生成深度图：
python ./tools/test_depth.py --load_ckpt res50.pth --backbone resnet50
# 生成3d点云图:
python ./tools/test_shape.py --load_ckpt res50.pth --backbone resnet50

# 使用 ResNeXt101 backbone 框架生成3d图
# 生成深度图：
python ./tools/test_depth.py --load_ckpt res101.pth --backbone resnext101
# 生成3d点云图:
python ./tools/test_shape.py --load_ckpt res101.pth --backbone resnext101


# 查看输出结果
# 宿主机：
cd /mnt/data2/zy_2025/github_store/Minist_Test/test_images
# 容器内：
cd /model/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs
```


## docker 打包2
```bash
# 1.构建 dockerfile 文件
# 2.复制 docker 文件夹到 /mnt/data2/zy_2025/github_store/BridgeDepth 路径
cp -r /home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/docker /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS

# 3.打开代理 privoxy

# 4.构建镜像
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/docker
bash build_image.sh

# 5.启动容器
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/docker
bash run_container.sh

# 在容器中激活环境 myenv
conda activate myenv

# 运行文件，开始推理
cd /model/AdelaiDepth-main/LeReS/Minist_Test
# 使用 ResNet50 backbone 框架生成3d图
# 生成深度图：
python ./tools/test_depth.py --load_ckpt res50.pth --backbone resnet50
# 生成3d点云图:
python ./tools/test_shape.py --load_ckpt res50.pth --backbone resnet50

# 使用 ResNeXt101 backbone 框架生成3d图
# 生成深度图：
python ./tools/test_depth.py --load_ckpt res101.pth --backbone resnext101
# 生成3d点云图:
python ./tools/test_shape.py --load_ckpt res101.pth --backbone resnext101


# 输入：
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/Minist_Test/test_images
# 查看输出结果
# 宿主机：
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs
# 容器内：
cd /model/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs
```