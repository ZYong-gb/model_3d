import numpy as np
import torch
import open3d as o3d  # 用于读写点云文件
import turboreg_gpu  # NOTE: torch must be imported before turboreg_gpu
import os
# -------------------------------
# 1. Load input correspondences
# -------------------------------
kpts_src = torch.from_numpy(np.loadtxt('../demo_data/000_fpfh_kpts_src.txt')).cuda().float()
kpts_dst = torch.from_numpy(np.loadtxt('../demo_data/000_fpfh_kpts_dst.txt')).cuda().float()

# -------------------------------
# 2. Initialize TurboReg
# -------------------------------
reger = turboreg_gpu.TurboRegGPU(
    6000,      # max_N: Maximum number of correspondences
    0.012,     # tau_length_consis: consistency threshold for feature length/distance
    2000,      # num_pivot: Number of pivot points, K_1
    0.15,      # radius_nms: Radius for avoiding instability (NMS)
    0.1,       # tau_inlier: Inlier threshold for post-refinement
    "IN"       # eval_metric: Use "Inlier Number" as scoring metric
)

# -------------------------------
# 3. Run registration
# -------------------------------
trans = reger.run_reg(kpts_src, kpts_dst).cpu().numpy()  # 转为 numpy 数组

print("Estimated transformation matrix (4x4):")
print(trans)

# -------------------------------
# 4. Load original point clouds (for visualization and saving)
# -------------------------------

# src_pcd = o3d.io.read_point_cloud("../demo_data/000_pts_src.ply")
# dst_pcd = o3d.io.read_point_cloud("../demo_data/000_pts_dst.ply")
src_pcd = o3d.io.read_point_cloud("../demo_data/1-pcd.ply")
dst_pcd = o3d.io.read_point_cloud("../demo_data/2-pcd.ply")

# -------------------------------
# 5. Apply transformation to source point cloud
# -------------------------------
src_aligned = src_pcd.transform(trans)  # 将源点云变换到目标坐标系

# -------------------------------
# 6. Save aligned point cloud to local file
# -------------------------------

from datetime import datetime
cur_time = datetime.now()
cur_time_format = cur_time.strftime("%Y-%m-%d_%H_%M_%S")
output_dir = "../out_trans_my"
os.makedirs(output_dir, exist_ok=True)  # 创建结果目录（如果不存在）

o3d.io.write_point_cloud(f"{output_dir}/src_aligned_{cur_time_format}.ply", src_aligned)
o3d.io.write_point_cloud(f"{output_dir}/dst_original_{cur_time_format}.ply", dst_pcd)  # 可选：也保存目标点云

# （可选）保存估计的变换矩阵
np.savetxt(f"{output_dir}/predicted_trans_{cur_time_format}.txt", trans)

print(f"✅ Aligned source point cloud saved to '{output_dir}/src_aligned_{cur_time_format}.ply'")
print(f"✅ Target point cloud saved to '{output_dir}/dst_original_{cur_time_format}.ply'")
print(f"✅ Predicted transformation saved to '{output_dir}/predicted_trans_{cur_time_format}.txt'")