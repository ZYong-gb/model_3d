# 容器使用步骤

## BridgeDepth
将单目深度估计与立体深度估计相结合，通过左右两张双目图片，得到深度图，3d点云图和视差图
```bash
# 进入路径
cd /mnt/data2/zy_2025/github_store/BridgeDepth/docker
# 启动容器
bash run_contain.sh
# 在容器中启动虚拟环境：myenv
conda activate myenv
# 执行脚本生成深度图
python infer.py --input ./assets/input_images/left_images_512x384/ ./assets/input_images/right_images_512x384/ --output ./docker_demo_output --from-pretrained ./checkpoints/bridge_rvc_pretrain.pth

# 查看输出结果
# 容器内：
ls /model/BridgeDepth/docker_demo_output
# 宿主机卷挂载：
ls /mnt/data2/zy_2025/github_store/BridgeDepth/docker_demo_output
```

## Depth-Anything-V2
单目相机，深度图，最终输出为rgb图像的深度图
```bash
# 运行容器
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker
bash run_container.sh

# 查看输出结果
# 宿主机卷挂载：
cd /mnt/data2/zy_2025/github_store/Depth-Anything-V2-main/docker_demo_output
# 容器内：
cd /model/Depth-Anything-V2/docker_demo_output
```

