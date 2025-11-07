# 项目-点云配准： 3D_multiview_reg
该代码库提供了用于训练和评估 LMPCR 算法的代码及数据。LMPCR 是首个能够以全局一致的方式对原始点云进行多视图配准的端到端算法。该代码库实现了相关论文中提出的算法逻辑，是该算法的官方实现版本。

## 克隆项目
```bash
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/zgojcic/3D_multiview_reg.git

```

## 环境准备
```bash
cd /mnt/data2/zy_2025/github_store/3D_multiview_reg
# 创建环境
conda create -n lmpr python=3.7 -y
conda activate lmpr

# 安装依赖包
pip install -r requirements.txt
pip install open3d==0.9.0.0
pip install scikit-learn
pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

# conda install -c open3d-admin open3d=0.9.0.0
# conda install -c intel scikit-learn
# conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

