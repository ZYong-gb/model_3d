# 模型 Damo_XR_Lab/Syncdreamer 使用步骤

## 创建虚拟环境
### 进入文件夹路径
cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/Syncdreamer
### 创建环境
conda create -n Syncdreamer python=3.10 -y
### 激活虚拟环境
conda activate Syncdreamer
### 安装依赖包
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


## 从 modelscope 上下载模型
### 进入文件夹路径
cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/Syncdreamer
### 下载模型
python Syncdreamer_load.py

## 模型使用
### 进入文件夹路径
cd /home/zqdl_ai2060/zy_account/model_3d/model_examples/Syncdreamer
### 运行文件
python syncdreamer_run.py