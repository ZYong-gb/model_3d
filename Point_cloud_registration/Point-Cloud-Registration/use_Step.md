# Point-Cloud-Registration
项目实现了 ICP（迭代最近点）算法，用于点云的三维配准。

## 克隆项目
```bash
cd /mnt/data2/zy_2025/github_store
git clone https://github.com/ReillyBova/Point-Cloud-Registration.git
```

## 环境准备
```bash
cd /mnt/data2/zy_2025/github_store/Point-Cloud-Registration
conda create -n Point-Cloud-Registration python=3.10 -y
conda activate Point-Cloud-Registration

pip install numpy
```

## 运行
```bash
python3 icp.py ./bunny/bun000.pts ./bunny/bun090.pts
```
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Point-Cloud-Registration/bunny D:\images\Point-Cloud-Registration
scp -P 11202 -r zqdl_ai2060@183.221.0.158:/mnt/data2/zy_2025/github_store/Point-Cloud-Registration/output D:\images\Point-Cloud-Registration

