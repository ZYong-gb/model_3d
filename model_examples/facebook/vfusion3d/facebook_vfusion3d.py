import torch
from transformers import AutoModel, AutoProcessor

# model_path = "../model_store_dir/facebook/vfusion3d"
model_path = "/mnt/data2/zy_2025/model_store_dir/facebook/vfusion3d"
model = AutoModel.from_pretrained(model_path,trust_remote_code=True)
processor = AutoProcessor.from_pretrained(model_path)
# 图像处理部分
# 加载图像
from PIL import Image
image_path = "../../../images/pic/1b4037e6347290b55b5bd8462c44f97.jpg"
image = Image.open(image_path).convert("RGB")

# preprocess the image and get the source camera 
image, source_camera = processor(image)  

# # generate planes (default output)
# output_planes = model(image, source_camera)
# print("Planes shape:", output_planes.shape)

# from datetime import datetime
# now = datetime.now()
# cur_time = now.strftime("%Y-%s-%D_%H-%M-%S")
# out_path = f"/home/zqdl_ai2060/zy_account/model_3d/images/output_{cur_time}.ply"

# generate a 3D mesh
output_planes, mesh_path = model(image, source_camera, export_mesh=True)
print("output_planes:",output_planes)
print("Planes shape:", output_planes.shape)
print("Mesh saved at:", mesh_path)

# # Generate a video
# output_planes, video_path = model(image, source_camera, export_video=True)
# print("Planes shape:", output_planes.shape)
# print("Video saved at:", video_path)