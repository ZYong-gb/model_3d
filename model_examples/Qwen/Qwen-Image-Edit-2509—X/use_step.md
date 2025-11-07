
# 模型 Qwen-Image-Edit-2509 使用步骤
## 进入虚拟环境
conda activate mapanything

## 开始执行
python Qwen-Image-Edit-2509_hf.py

### 运行结果：显存不足
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 130.00 MiB. GPU 0 has a total capacity of 11.74 GiB of which 82.75 MiB is free. Including non-PyTorch memory, this process has 11.55 GiB memory in use. Of the allocated memory 11.30 GiB is allocated by PyTorch, and 166.65 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)