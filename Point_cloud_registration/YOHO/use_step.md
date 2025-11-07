# YOHO


## git clone
```bash
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/HpWang-whu/YOHO.git


conda create -n fcgf_yoho python=3.10 -y
conda activate fcgf_yoho

# python 3.7
pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
# python 3.10
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121

export http_proxy=http://2.2.2.122:8118
export https_proxy=http://2.2.2.122:8118
pip install git+https://github.com/NVIDIA/MinkowskiEngine.git


```