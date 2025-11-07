import cv2
import torch
# from moge.model.v1 import MoGeModel
from moge.model.v2 import MoGeModel # Let's try MoGe-2


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = "cpu"
# Load the model from huggingface hub (or load from local).
local_model_path = "/mnt/data2/zy_2025/github_store/MoGe/Ruicheng/moge-2-vitl-normal/model.pt"   # 使用本地路径

model = MoGeModel.from_pretrained(local_model_path,local_files_only=True).to(device)                             



# Read the input image and convert to tensor (3, H, W) with RGB values normalized to [0, 1]
input_image = cv2.cvtColor(cv2.imread("/mnt/data2/zy_2025/github_store/MoGe/assets/pic/1b4037e6347290b55b5bd8462c44f97.jpg"), cv2.COLOR_BGR2RGB)                       
input_image = torch.tensor(input_image / 255, dtype=torch.float32, device=device).permute(2, 0, 1)    
# print("input_image:",input_image)

# Infer 
output = model.infer(input_image)
"""
`output` has keys "points", "depth", "mask", "normal" (optional) and "intrinsics",
The maps are in the same size as the input image. 
{
    "points": (H, W, 3),    # point map in OpenCV camera coordinate system (x right, y down, z forward). For MoGe-2, the point map is in metric scale.
    "depth": (H, W),        # depth map
    "normal": (H, W, 3)     # normal map in OpenCV camera coordinate system. (available for MoGe-2-normal)
    "mask": (H, W),         # a binary mask for valid pixels. 
    "intrinsics": (3, 3),   # normalized camera intrinsics
}
"""


