import cv2
import torch
import numpy as np
from depth_anything_v2.dpt import DepthAnythingV2

# 设置设备
DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

# 模型配置
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

# 选择模型
encoder = 'vitl'
model = DepthAnythingV2(**model_configs[encoder])
model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
model = model.to(DEVICE).eval()

# 读取图像
raw_img = cv2.imread('assets/examples/demo01.jpg')  # 替换为你的图像路径

# 推理
depth = model.infer_image(raw_img)  # (H, W) numpy array

# # 可视化：归一化到 0~255 并转为伪彩色
# depth_vis = (depth - depth.min()) / (depth.max() - depth.min())  # 归一化
# depth_vis = (depth_vis * 255).astype(np.uint8)  # 转为 0~255
# depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_INFERNO)  # 伪彩色


# 保存结果
from datetime import datetime
now_time = datetime.now()
format_time = now_time.strftime("%Y-%m-%d-%H_%M_%S")
out_path = f"assets/out_images/depth_{format_time}.png"
cv2.imwrite(out_path, depth)
print(f"深度图已保存为 {out_path}")