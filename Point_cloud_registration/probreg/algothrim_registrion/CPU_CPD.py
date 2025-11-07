import copy
import numpy as np
import open3d as o3d
from probreg import cpd

source_path = "/mnt/data2/zy_2025/github_store/AdelaiDepth/docker/Minist_Test/test_images/outputs/1-pcd.ply"
target_path = "/mnt/data2/zy_2025/github_store/AdelaiDepth/docker/Minist_Test/test_images/outputs/2-pcd.ply"
output_path = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/registered_source.ply"

print("Loading point clouds...")
source = o3d.io.read_point_cloud(source_path)
target = o3d.io.read_point_cloud(target_path)

source.remove_non_finite_points()
target.remove_non_finite_points()

# ⚠️ 注意：voxel_size=100 极可能过大！先检查点云尺度
print("Source bounds:", source.get_min_bound(), "to", source.get_max_bound())
print("Target bounds:", target.get_min_bound(), "to", target.get_max_bound())

voxel_size = 50.0  # 假设单位是毫米（常见于深度图生成的点云），5cm 降采样
if voxel_size > 0:
    source_down = source.voxel_down_sample(voxel_size=voxel_size)
    target_down = target.voxel_down_sample(voxel_size=voxel_size)
else:
    source_down = source
    target_down = target

print(f"Downsampled: source={len(source_down.points)}, target={len(target_down.points)}")

print("Running CPD registration...")
tf_param, _, _ = cpd.registration_cpd(source_down, target_down)

print("Applying transformation to original source...")
# ✅ 修复：正确转换类型
original_points = np.asarray(source.points)
transformed_points = tf_param.transform(original_points)
result = copy.deepcopy(source)
result.points = o3d.utility.Vector3dVector(transformed_points)  # ←←← 关键行！

print(f"Saving registered point cloud to {output_path}...")
o3d.io.write_point_cloud(output_path, result)
print("✅ Done!")