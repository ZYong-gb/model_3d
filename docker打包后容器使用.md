# 容器使用步骤
## AdelaiDepth
生成3d点云图，单目相机
```bash
# 启动容器
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/docker
bash run_container.sh

# 在容器中激活环境 myenv
conda activate myenv

# 运行文件，开始推理
cd /model/AdelaiDepth-main/LeReS/Minist_Test

# 生成深度图：
python ./tools/test_depth.py --load_ckpt res50.pth --backbone resnet50
python ./tools/test_depth.py --load_ckpt res101.pth --backbone resnext101


# 输入：
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/Minist_Test/test_images
# 查看输出结果：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs
# 容器内：
cd /model/AdelaiDepth-main/LeReS/Minist_Test/test_images/outputs
```

## FoundationStereo 
生成点云图,双目相机
```bash
# 运行容器
cd /mnt/data2/zy_2025/github_store/FoundationStereo/docker_2
bash run_container.sh
# 运行后可视化部分会产生警告，这是正常的

# 查看输出结果图片：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/FoundationStereo/docker_demo_output
# 容器内部：
cd /model/FoundationStereo/docker_demo_output
```

## BridgeDepth
将单目深度估计与立体深度估计相结合，通过左右两张双目图片，得到深度图，3d点云图和视差图
```bash
# 进入路径
cd /mnt/data2/zy_2025/github_store/BridgeDepth/docker
# 启动容器
bash run_contain.sh
# 在容器中启动虚拟环境：myenv
conda activate myenv
# 启动代理
# export http_proxy=http://2.2.2.110:8118
# export https_proxy=http://2.2.2.110:8118

# 执行脚本生成深度图
python infer.py --input ./assets/input_images/left_images_512x384/ ./assets/input_images/right_images_512x384/ --output ./docker_demo_output --from-pretrained ./checkpoints/bridge_rvc_pretrain.pth


# 查看输出结果图片：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/BridgeDepth/docker_demo_output
# 容器内部：
cd /model/BridgeDepth/docker_demo_output
```

## Depth-Anything-V2
单目相机，深度图，最终输出为rgb图像的深度图
```bash
# 启动容器
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker
bash run_container.sh

# 查看输出结果
# 宿主机卷挂载：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output
# 容器内：
cd /model/Depth-Anything-V2/docker_demo_output
```

## MoGe
能够从单目开放域图像中恢复出三维几何信息，包括测距点云、测距深度图、法线图以及相机的视场角等信息。
```bash
# 清理输出缓存
cd /mnt/data2/zy_2025/github_store/MoGe/docker_demo_output
rm -rf *

# 启动容器
cd /mnt/data2/zy_2025/github_store/MoGe/docker
bash run_container.sh

# 查看输出结果
# 宿主机卷挂载：
# /mnt/data2/zy_2025/github_store/MoGe/docker_demo_output:/model/MoGe/docker_demo_output

# 查看输出结果图片：
# 宿主机：
cd /mnt/data2/zy_2025/github_store/MoGe/docker_demo_output
# 容器内部：
cd /model/MoGe/docker_demo_output
```


## TurboReg
点云配准，运行后输出结果为：目标点云、源点云以及变换矩阵
```bash
# 运行容器
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

## TurboReg
点云配准，运行后输出结果为：目标点云、源点云以及变换矩阵
```bash
# 运行容器
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/docker
bash run_container.sh


# 容器内部运行：
cd /model/Depth-Anything-3
conda activate myenv
# 设置环境变量强制离线模式 加载模型
# transformers 库不联网
export TRANSFORMERS_OFFLINE=1
# datasets 库不联网
export HF_DATASETS_OFFLINE=1
# 所有 Hugging Face 相关操作强制离线（最彻底）
export HF_HUB_OFFLINE=1
# 设置环境变量
# 设置本地模型存储路径
export MODEL_DIR=/model/Depth-Anything-3/checkpoints/DA3NESTED-GIANT-LARGE/
# 设置输出目录
export GALLERY_DIR=workspace/gallery
mkdir -p $GALLERY_DIR

# 开始推理1
da3 auto assets/examples/SOH \
    --export-format glb \
    --export-dir ${GALLERY_DIR}/examples/SOH \
    --model-dir ${MODEL_DIR}

# 开始推理2
da3 auto assets/examples/zqdl_shinei \
    --export-format glb-npz \
    --export-dir ${GALLERY_DIR}/examples/zqdl_shinei/ \
    --model-dir ${MODEL_DIR} \
    --device cuda:1 \
    --auto-cleanup

# --device 参数: cpu, cuda, ipu, xpu, mkldnn, opengl, opencl, ideep, hip, ve, fpga, ort, xla, lazy, vulkan, mps, meta, hpu, mtia ,无实现多卡代码

# 输出结果卷挂载：
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/assets:/model/Depth-Anything-3/assets \
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace:/model/Depth-Anything-3/workspace \
    # -v /mnt/data2/zy_2025/github_store/Depth-Anything-3/checkpoints:/model/Depth-Anything-3/checkpoints \
    
# 查看图片，宿主机：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-3/workspace
# 查看图片，容器中：
cd /model/Depth-Anything-3/workspace
```