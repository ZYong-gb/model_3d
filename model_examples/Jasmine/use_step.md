
# 模型 jasmine 使用步骤,python命令行版
利用扩散先验进行自监督深度估计


## 设置国外代理加速下载文件
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.122:8118 http_proxy=http://2.2.2.122:8118
```


## github 项目下载
```bash
cd /mnt/data2/zy_2025/model_store_dir
git clone https://github.com/wangjiyuan9/Jasmine.git
```
- 项目存储路径：/mnt/data2/zy_2025/model_store_dir/Jasmine


## 环境配置
### 从 huggingface 下载已经配置好的环境，到 minconda/envs
```bash
# 进入 jasmine 的存储路径
cd /mnt/data2/zy_2025/model_store_dir/Jasmine

# Download the conda-packed environment
wget https://huggingface.co/exander/Jasmine/resolve/main/jasmine.tar.gz
# 或者
git clone https://huggingface.co/exander/Jasmine
# 或者直接在 hunggingface 网站通过鼠标点击下载

# 将下载的 文件通过 scp 传到 /mnt/data2/zy_2025/model_store_dir/jasmine 路径
scp -P 11202 -r D:\project_all\jasmine\checkpoints\* zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/model_store_dir/Jasmine

# Create directory and extract
cd /mnt/data2/zy_2025/model_store_dir/Jasmine
mkdir -p /mnt/data2/work/miniconda3/envs/jasmine
tar -xzf jasmine.tar.gz -C /mnt/data2/work/miniconda3/envs/jasmine

# Activate the environment
conda activate jasmine

# 安装依赖包
pip install -r requirements.txt
```

### 从 huggingface 下载预训练模型
```bash
# Download the model checkpoint
wget https://huggingface.co/exander/Jasmine/resolve/main/Jasmine.zip
# 或者直接在 hunggingface 网站通过鼠标点击下载
# 将下载的 文件通过 scp 传到 /mnt/data2/zy_2025/model_store_dir/jasmine 路径
scp -P 11202 -r D:\project_all\jasmine\checkpoints\* zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/model_store_dir/Jasmine

unzip Jasmine.zip -d ckpt/
```

### 将图片数据传到 /mnt/data2/zy_2025/model_store_dir/Jasmine
```bash
mkdir -p data/KITTI
scp -P 11202 D:\project_all\jasmine\data\KITTI\2011_09_26_drive_0001_extract.zip zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/model_store_dir/Jasmine/data/KITTI
cd /mnt/data2/zy_2025/model_store_dir/Jasmine/data/KITTI
unzip 2011_09_26_drive_0001_extract.zip
```


## 模型运行
```bash
cd /mnt/data2/zy_2025/model_store_dir/Jasmine
conda activate jasmine

python trains.py --only_test --eval_split eigen \
    --ug --link_mode first \
    --data_path /mnt/data2/zy_2025/model_store_dir/Jasmine/data/KITTI/2011_09_26/2011_09_26_drive_0001_extract/image_00 \
    --resume_from_checkpoint ./ckpt/

```

### 改错
```bash
pip install timm
pip install --upgrade diffusers peft accelerate
pip install --upgrade transformers
```
### 运行结果
- 项目中缺少 optimizer.bin 文件（未给出）
- FileNotFoundError: [Errno 2] No such file or directory: 'ckpt/optimizer.bin'