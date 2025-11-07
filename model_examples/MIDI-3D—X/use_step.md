# model 使用步骤
## 创建虚拟环境
- conda create -n midi python=3.10 -y
- conda activate midi
## 克隆github上的仓库
- git clone https://github.com/VAST-AI-Research/MIDI-3D.git /mnt/data2/zy_2025/github_store/MIDI-3D
- 存储路径：/mnt/data2/zy_2025/github_store/MIDI-3D
## 安装必要的软件包
- cd /mnt/data2/zy_2025/github_store/MIDI-3D
- pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
- pip install "pyparsing>=2.3.1" "pandas>=1.2"
### 升级 GCC
- conda install -c conda-forge gcc=11 gxx=11
- pip install -r requirements.txt
## 为了生成具有纹理效果的三维场景，需要安装MV-Adapter。
pip install git+https://github.com/huanngzh/MV-Adapter
### 请确保 gradio 的版本号为 1.0。如果安装 mvadapter 会导致 gradio 的版本号发生变化，那么务必重新安装 gradio。
pip list | grep gradio
## Launch Demo
python gradio_demo.py

## 缺失包补充
- pip install git+https://github.com/NVlabs/nvdiffrast
- pip install jaxtyping
- pip install pymeshlab==2022.2

## Launch Demo
python gradio_demo.py
### 运行结果：显存不够
GPU 0 has a total capacity of 11.74 GiB of which 6.75 MiB is free. Including non-PyTorch memory, this process has 11.62 GiB memory in use. Of the allocated memory 11.14 GiB is allocated by PyTorch, and 408.84 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)