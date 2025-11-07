import numpy as np
import open3d as o3d
import time

use_cuda = True

if use_cuda:
    import cupy as cp
    to_cpu = cp.asnumpy
    cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
else:
    cp = np
    to_cpu = lambda x: x

from probreg import cpd


def load_and_downsample_ply_with_color(filename, voxel_size=2.0):
    """
    加载 .ply 点云，下采样，并返回 points 和 colors。
    如果原始点云无颜色，则返回 None。
    """
    pcd = o3d.io.read_point_cloud(filename)
    if pcd.is_empty():
        raise ValueError(f"无法加载点云文件: {filename}")
    
    has_color = pcd.has_colors()
    print(f"  原始点数: {len(pcd.points)}，包含颜色: {has_color}")

    # 执行下采样（会自动同步 points 和 colors）
    pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
    
    points = np.asarray(pcd_down.points, dtype=np.float32)
    colors = np.asarray(pcd_down.colors, dtype=np.float32) if pcd_down.has_colors() else None

    print(f"  下采样后点数: {len(points)} (voxel_size={voxel_size})")
    return points, colors


def save_point_cloud_ply_with_color(points, colors, filename):
    """保存带颜色的点云"""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if colors is not None and len(colors) == len(points):
        pcd.colors = o3d.utility.Vector3dVector(colors)
    else:
        print("  警告: 颜色数据缺失或长度不匹配，保存为无颜色点云。")
    o3d.io.write_point_cloud(filename, pcd, write_ascii=False)


# ——————————————————————————————
# 文件路径
# ——————————————————————————————
source_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/1-pcd.ply"
target_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/2-pcd.ply"
registered_source_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/Affine_CPD_Moge_registered_source.ply"
combined_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/Affine_CPD_Moge_combined.ply"

# ——————————————————————————————
# 加载并下采样（带颜色）
# ——————————————————————————————
print("正在加载并下采样点云（含颜色）...")
voxel_size = 0.1
source_points, source_colors = load_and_downsample_ply_with_color(source_file, voxel_size=voxel_size)
target_points, target_colors = load_and_downsample_ply_with_color(target_file, voxel_size=voxel_size)

# ——————————————————————————————
# 转到 GPU / CPU（仅坐标用于配准）
# ——————————————————————————————
print("准备数据...")
source_gpu = cp.asarray(source_points, dtype=cp.float32)
target_gpu = cp.asarray(target_points, dtype=cp.float32)

# ——————————————————————————————
# AffineCPD 配准（只用坐标）
# ——————————————————————————————
print("开始 AffineCPD 配准...")
acpd = cpd.AffineCPD(source_gpu, use_cuda=use_cuda)

start_time = time.time()
tf_param, _, _ = acpd.registration(target_gpu)
elapsed_time = time.time() - start_time
print(f"配准完成！耗时: {elapsed_time:.3f} 秒")

# ——————————————————————————————
# 应用变换到 source 坐标（颜色不变）
# ——————————————————————————————
source_transformed_points = to_cpu(tf_param.transform(source_gpu))
# source_colors 保持不变！

# ——————————————————————————————
# 保存配准后的 source（带颜色）
# ——————————————————————————————
save_point_cloud_ply_with_color(source_transformed_points, source_colors, registered_source_file)
print(f"配准结果已保存至: {registered_source_file}")

# ——————————————————————————————
# 融合点云：拼接 points 和 colors
# ——————————————————————————————
combined_points = np.vstack([source_transformed_points, target_points])

# 融合颜色：如果任一无颜色，则整体无颜色
if source_colors is not None and target_colors is not None:
    combined_colors = np.vstack([source_colors, target_colors])
else:
    combined_colors = None
    print("融合点云将不包含颜色（至少一个输入无颜色）。")

# 保存融合结果
save_point_cloud_ply_with_color(combined_points, combined_colors, combined_file)
print(f"融合点云已保存至: {combined_file}")
print(f"最终融合点数: {combined_points.shape[0]}")