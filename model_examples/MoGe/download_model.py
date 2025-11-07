import os  
from huggingface_hub import snapshot_download  

# 设置目标目录  
target_dir = "/mnt/data2/zy_2025/github_store/MoGe/checkpoints/moge-2-vitl-normal"  

# 确保目标目录存在  
if not os.path.exists(target_dir):  
    os.makedirs(target_dir, exist_ok=True)  
    print(f"Created directory: {target_dir}")  
else:  
    print(f"Directory already exists: {target_dir}")  

# 执行下载  
try:  
    snapshot_download(  
        repo_id="Ruicheng/moge-2-vitl-normal",  
        local_dir=target_dir,  
        local_dir_use_symlinks=False  
    )  
    print("Download completed successfully.")  
except Exception as e:  
    print(f"Error during download: {str(e)}")