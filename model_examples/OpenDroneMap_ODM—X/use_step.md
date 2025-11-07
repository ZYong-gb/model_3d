# 项目 OpenDroneMap/ODM 使用步骤

## 使用 docker 拉取项目运行
### 拉取镜像
sudo docker pull opendronemap/odm

## 使用 git 下载项目运行
### 项目下载
```bash
# 进入文件保存目录
cd /mnt/data2/zy_2025/github_store
# 在命令行依次输入以下代码，即可配置国外代理
export https_proxy=http://2.2.2.110:8118
export http_proxy=http://2.2.2.110:8118
# 克隆项目 ODM
git clone https://github.com/OpenDroneMap/ODM.git
```
### 创建环境
conda create -n odm python=3.10 -y
### 激活虚拟环境
conda activate odm

### 项目运行
```bash
# 进入项目文件夹
cd /mnt/data2/zy_2025/github_store/ODM
bash configure.sh install
# 运行项目生成3d模型

```