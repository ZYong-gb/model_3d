# 模型 BoRe-Depth 使用步骤,python命令行版
一种轻量级的单目深度估计方法

## 克隆github上的仓库
### 进入项目文件保存目录
cd /mnt/data2/zy_2025/github_store
### 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118 http_proxy=http://2.2.2.110:8118
env | grep -i proxy
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
```
### 使用 git 克隆项目
git clone https://github.com/liangxiansheng093/BoRe-Depth.git
- 项目存储路径：/mnt/data2/zy_2025/github_store/BoRe-Depth


### 环境配置
```bash
cd /mnt/data2/zy_2025/github_store/BoRe-Depth
conda create -n BoRe_Depth python=3.10 -y
conda activate BoRe_Depth
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install pytorch-lightning==1.9.0

# 进入 requirements.txt 文件中，注释掉：
# pytorch==2.0.1
# torchvision
# pytorch-lightning==1.9.0
# mmcv-full==1.4

pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

pip install mmcv==2.2.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.3/index.html
```

###  项目运行
<!-- #### 模型训练
```bash
python test.py --dataset_name nyu --dataset_dir datasets/nyu/testing --ckpt_path checkpoints/nyu.ckpt
```
选项：
- --dataset_name：[纽约大学、基特大学、iBims]。根据所选数据集生成的深度图的大小。
- --dataset_dir：通往测试数据集的路径（支持 jpg 和 png 两种格式）。
- --ckpt_path：通往训练后模型权重的路径。 -->

#### 模型使用测试
```bash
python infer.py --dataset_name nyu --ckpt_path checkpoints/nyu.ckpt --input_dir demo --output_dir output --save-vis --save-depth
```
选项：
- --dataset_name：[纽约大学、基特大学、iBims]。根据所选数据集生成的深度图的大小。
- --ckpt_path：通往训练后模型权重的路径。
- --input_dir：输入图片或文件夹的路径（支持 jpg 和 png 两种格式）。
- --output_dir：输出深度图的生成路径（支持 png 和 npy 两种格式）。
- --save-vis：保存这些视觉图像。
- --save-depth：保存 NumPy 计算得到的结果。

### 结果
模型 checkpoints/*.ckpt 文件未给出，需要提出申请，已申请查看，暂未反馈