#模型下载
from modelscope import snapshot_download

model_dir = snapshot_download('facebook/map-anything',local_dir="../model_store_dir/facebook/map-anything")

# 模型下载不完整

# 项目地址：
# https://github.com/facebookresearch/map-anything/tree/main