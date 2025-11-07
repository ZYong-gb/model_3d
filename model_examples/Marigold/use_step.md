# Marigold 
Marigold——是一套基于条件生成模型的技术体系，同时也配套了一套微调方案。该方案能够从预训练的潜在扩散模型（如 Stable Diffusion）中提取所需知识，并将这些模型适配用于密集图像分析任务，包括单目深度估计、表面法线预测以及图像内在结构分析等。

## clone
```bash
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/prs-eth/Marigold.git

cd /mnt/data2/zy_2025/github_store/Marigold
conda create -n marigold python=3.10 -y
conda activate marigold

pip install -r requirements.txt
```

## download checkpoints
```bash
cd /mnt/data2/zy_2025/github_store/Marigold

export http_proxy=http://2.2.2.122:8118 \
    https_proxy=http://2.2.2.122:8118
    
bash script/download_weights.sh marigold-depth-v1-1           # depth checkpoint
bash script/download_weights.sh marigold-normals-v1-1         # normals checkpoint
bash script/download_weights.sh marigold-iid-appearance-v1-1  # iid appearance checkpoint
bash script/download_weights.sh marigold-iid-lighting-v1-1    # iid lighting checkpoint
# bash script/download_weights.sh marigold-depth-v1-0         # CVPR depth checkpoint
```

## run demo
### Depth
```bash
cd /mnt/data2/zy_2025/github_store/Marigold
conda activate marigold

python script/depth/run.py \
    --checkpoint prs-eth/marigold-depth-v1-1 \
    --input_rgb_dir input/in-the-wild_example \
    --output_dir output/in-the-wild_example \
    --fp16

```