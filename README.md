# 3d 重建—model
在 model_examples 文件夹下存放模型运行项目

## right model
- model_3d/model_examples/AdelaiDepth-main：生成3d点云图，单目
- model_3d/model_examples/facebook/dinov2_base
- model_3d/model_examples/facebook/vfusion3d

- model_3d/model_examples/FoundationStereo：生成点云图,双目相机
- model_3d/model_examples/Depth-Anything-V2：生成深度图，单目
- model_3d/model_examples/MoGe：能够从单目开放域图像中恢复出三维几何信息，包括测距点云、测距深度图、法线图以及相机的视场角等信息。
- model_3d/model_examples/BridgeDepth：需双目相机，输出3d点云图，深度图，视差图
- model_3d/model_examples/TurboReg：3D点云配准算法项目
- model_3d/model_examples/VisFusion： 通过RGB、深度、相机位姿和内参数据实时重建3d模型（训练的ckpt用于高质量重建）
- model_3d/model_examples/Marigold: 密集图像分析任务，包括单目深度估计、表面法线预测以及图像内在结构分析（模型下载太慢）
- OpenPCDet :3d 物体检测算法，专门用于基于激光雷达的3D物体检测。
- model_3d/model_examples/Depth-Anything-3 : 生成深度图以及使用多视图RGB和深度图生成融合后的3d点云数据，（官方仅提供单卡推理实现）

## mistake model
### model_3d/model_examples/facebook/map_anything—X
- 环境配置失败
### model_3d/model_examples/MIDI-3D—X
- 运行结果，显存不够
GPU 0 has a total capacity of 11.74 GiB of which 6.75 MiB is free. Including non-PyTorch memory, this process has 11.62 GiB memory in use. Of the allocated memory 11.14 GiB is allocated by PyTorch, and 408.84 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
### model_3d/model_examples/Tencent-Hunyuan/Hunyuan3D-2—X
- 运行结果：
ModuleNotFoundError: No module named 'hy3dgen'
### model_3d/model_examples/Qwen/Qwen-Image-Edit-2509—X
- 运行结果：显存不足
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 130.00 MiB. GPU 0 has a total capacity of 11.74 GiB of which 82.75 MiB is free. Including non-PyTorch memory, this process has 11.55 GiB memory in use. Of the allocated memory 11.30 GiB is allocated by PyTorch, and 166.65 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
### model_3d/model_examples/NeuralRecon—X
- 环境配置失败
### model_3d/model_examples/TripoSR—X
- 环境配置失败


### model_3d/model_examples/BoRe-Depth—X
- 模型 checkpoints/*.ckpt 文件未给出，需要提出申请，已申请查看，暂未反馈
### model_3d/model_examples/Jasmine
- 项目中缺少 optimizer.bin 文件（未给出）
- FileNotFoundError: [Errno 2] No such file or directory: 'ckpt/optimizer.bin'



