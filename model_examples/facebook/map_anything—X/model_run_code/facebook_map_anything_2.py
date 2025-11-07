import sys
import os

# 替换为实际模型路径
packages_path = "/home/zqdl_ai2060/zy_account/model_3d/model_store_dir/facebook/map-anything"
if os.path.exists(packages_path) and packages_path not in sys.path:
    sys.path.insert(0, packages_path)  # 优先搜索此路径

# 验证导入
from mapanything.models import MapAnything
import torch  
from mapanything.models import MapAnything  
from mapanything.utils.image import load_images  
import glob  

# Get inference device  
device = "cuda" if torch.cuda.is_available() else "cpu"  



# Optional config for better memory efficiency  
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"  
  
  
  
# Init model - This requires internet access or the huggingface hub cache to be pre-downloaded  
# For Apache 2.0 license model, use "facebook/map-anything-apache"  
model_path = "../model_store_dir/facebook/map-anything"  
# 离线下，加载本地模型  
from transformers import AutoConfig  
config = AutoConfig.from_pretrained(model_path)  
model = MapAnything(config).to(device)  
  
# Load and preprocess images from a folder  
images_path = "../images/pic/"  # 改为文件夹路径  
image_files = glob.glob(os.path.join(images_path, "*.jpg"))  # 获取所有jpg文件  
views = load_images(image_files)  # 加载多张图片  
  
# Run inference with memory efficient mode  
predictions = model.infer(  
    views,                              
    memory_efficient_inference=True,  # 启用内存高效模式  
    use_amp=True,                       
    amp_dtype="bf16",                   
    apply_mask=True,                    
    mask_edges=True,                    
    apply_confidence_mask=False,        
    confidence_percentile=10,           
)  
  
# 创建保存结果的文件夹  
output_dir = "../images/output_image/"  
os.makedirs(output_dir, exist_ok=True)  
  
# Access and save results for each view  
for i, pred in enumerate(predictions):  
    # 保存原始输入图像  
    input_img = pred["img_no_norm"]  
    torch.save(input_img, os.path.join(output_dir, f"input_img_{i}.pt"))  
      
    # 保存3D点云数据  
    pts3d = pred["pts3d"]  
    torch.save(pts3d, os.path.join(output_dir, f"pts3d_{i}.pt"))  
      
    # 保存深度图  
    depth_z = pred["depth_z"]  
    torch.save(depth_z, os.path.join(output_dir, f"depth_z_{i}.pt"))  
      
    # 保存置信度图  
    confidence = pred["conf"]  
    torch.save(confidence, os.path.join(output_dir, f"confidence_{i}.pt"))  
      
    # 保存掩码图  
    mask = pred["mask"]  
    torch.save(mask, os.path.join(output_dir, f"mask_{i}.pt"))  
      
    # 保存相机位姿  
    camera_poses = pred["camera_poses"]  
    torch.save(camera_poses, os.path.join(output_dir, f"camera_poses_{i}.pt"))  
      
    # 保存内参矩阵  
    intrinsics = pred["intrinsics"]  
    torch.save(intrinsics, os.path.join(output_dir, f"intrinsics_{i}.pt"))  
  
print(f"Results saved to {output_dir}")