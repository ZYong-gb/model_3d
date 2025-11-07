import os
import torch
from PIL import Image
from modelscope import QwenImageEditPlusPipeline

model_path = "../model_store_dir/Qwen/Qwen-Image-Edit-2509"
model_path = "/mnt/data2/zy_2025/model_store_dir/Qwen/Qwen-Image-Edit-2509"
pipeline = QwenImageEditPlusPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
print("pipeline loaded")

pipeline.to('cuda')
pipeline.set_progress_bar_config(disable=None)
image1 = Image.open("../images/photo_man/3.png")
image2 = Image.open("../images/photo_man/4.png")
prompt = "The magician bear is on the left, the alchemist bear is on the right, facing each other in the central park square."
inputs = {
    "image": [image1, image2],
    "prompt": prompt,
    "generator": torch.manual_seed(0),
    "true_cfg_scale": 4.0,
    "negative_prompt": " ",
    "num_inference_steps": 40,
    "guidance_scale": 1.0,
    "num_images_per_prompt": 1,
}

from datetime import datetime  
# 获取当前时间  
current_time = datetime.now()  
# 格式化并打印时间  
formatted_time = current_time.strftime('%Y_%m_%d_%H_%M')  

with torch.inference_mode():
    output = pipeline(**inputs)
    output_image = output.images[0]
    output_image.save("../images/output_image/3.png")
    print("image saved at", os.path.abspath(f"../images/output_image/{formatted_time}.png"))
