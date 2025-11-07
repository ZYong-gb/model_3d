import torch

print("PyTorch版本:", torch.__version__)          # 示例: 2.0.1
print("PyTorch使用的CUDA版本:", torch.version.cuda) # 示例: 11.8
print("CUDA是否可用:", torch.cuda.is_available())  # 必须为True
print("GPU名称:", torch.cuda.get_device_name(0))   # 示例: NVIDIA GeForce RTX 3080
# torch.version.cuda 需与本地安装的CUDA Toolkit版本一致。
# torch.cuda.is_available() 为 True 表示PyTorch能正确调用CUDA。