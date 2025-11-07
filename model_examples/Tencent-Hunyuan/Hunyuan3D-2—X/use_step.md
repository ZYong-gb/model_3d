
# 模型 Tencent-Hunyuan/Hunyuan3D-2 使用步骤


## 设置代理
```bash
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118
export http_proxy=http://2.2.2.110:8118
```
## 模型从 modelscope 下载
python tencent_Hunyuan3D-2_load.py

## 创建虚拟环境
conda create -n hunyuan3d-2 python=3.12 -y
## 进入虚拟环境
conda activate hunyuan3d-2


## 开始执行
python hunyuan3d_2.py

### 运行结果：
ModuleNotFoundError: No module named 'hy3dgen'