from modelscope import AutoImageProcessor, AutoModel
from PIL import Image
import numpy as np
import torch

# 加载图像
image_path = "../../../images/photo_man/3.png"
image = Image.open(image_path).convert("RGB")

# 加载模型
# model_path = "../model_store_dir/facebook/dinov2-base"
model_path = "/mnt/data2/zy_2025/model_store_dir/facebook/dinov2-base"
processor = AutoImageProcessor.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

# 获取隐藏状态
inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
last_hidden_states = outputs.last_hidden_state

# 转换为图像
hidden_state = last_hidden_states[0].detach().numpy()  # 移除批次维度
hidden_state = (hidden_state - hidden_state.min()) / (hidden_state.max() - hidden_state.min()) * 255
image_output = Image.fromarray(hidden_state.astype(np.uint8))

from datetime import datetime
# 获取当前日期和时间
now = datetime.now()
cur_time = now.strftime("%Y-%m-%d-%H_%M_%S")
print("当前时间:", cur_time)

# 保存图像
output_path = f"../../../images/output_images/{cur_time}.png"  
image_output.save(output_path)
print(f"隐藏状态已保存为图像：{output_path}")

  