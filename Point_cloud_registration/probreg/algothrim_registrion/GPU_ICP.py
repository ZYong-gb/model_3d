


# # -*- coding: utf-8 -*-
# """
# 点云序列增量配准脚本
# 功能：
#   1. 读取 input_ply/ 下的 *-pcd.ply 文件（如 1-pcd.ply, 2-pcd.ply...）
#   2. 以第1帧为全局参考坐标系
#   3. 逐帧使用 GPU-ICP 配准到前一帧的配准结果
#   4. 保存每帧在全局坐标系下的结果（registered_001.ply, ...）
#   5. 合并所有配准后的点云，输出 final_registered_full.ply
# """

# import os
# import copy
# import numpy as np
# import open3d as o3d

# # ----------------------------
# # 1. 配置路径和参数
# # ----------------------------

# # 输入文件夹：存放原始点云（命名格式：1-pcd.ply, 2-pcd.ply, ...）
# input_folder = "../input_ply"

# # 输出文件夹：存放配准结果
# output_dir = "../output_ply"
# os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在则创建

# # ICP 配准参数
# voxel_size = 20.0                      # 体素降采样尺寸（单位：与点云一致，如毫米）
# max_correspondence_distance = 100.0    # ICP 最大对应点距离（单位同上）

# # ----------------------------
# # 2. 获取并排序输入文件
# # ----------------------------

# # 获取所有以 "-pcd.ply" 结尾的文件
# all_files = [f for f in os.listdir(input_folder) if f.endswith("-pcd.ply")]

# # 按文件名前缀的数字排序（如 "1-pcd.ply" -> 1, "10-pcd.ply" -> 10）
# all_files.sort(key=lambda x: int(x.split('-')[0]))

# # 检查是否至少有两个点云文件
# if len(all_files) < 2:
#     raise ValueError("输入文件夹中至少需要两个点云文件（如 1-pcd.ply, 2-pcd.ply）！")

# print(f"✅ 找到 {len(all_files)} 个点云文件: {all_files}")

# # ----------------------------
# # 3. 初始化：第1帧作为全局参考
# # ----------------------------

# # 构建第1个点云文件的完整路径
# first_pcd_path = os.path.join(input_folder, all_files[0])

# # 读取第1帧点云
# global_target = o3d.io.read_point_cloud(first_pcd_path)

# # 移除非法点（NaN / Inf）
# global_target.remove_non_finite_points()

# # 保存第1帧为 registered_001.ply（全局坐标系原点）
# init_output_path = os.path.join(output_dir, "Moge_registered_001.ply")
# o3d.io.write_point_cloud(init_output_path, global_target)
# print(f"✅ 初始化：将 {all_files[0]} 作为全局参考，保存为 {init_output_path}")

# # 初始化最终融合点云（包含所有配准后的点）
# final_combined_pcd = copy.deepcopy(global_target)

# # 初始化累计变换矩阵列表（每个元素是从原始帧到全局坐标系的变换）
# # 第1帧的变换是单位矩阵
# global_transforms = [np.eye(4)]

# # 当前累计变换（从当前处理帧的原始坐标系到全局坐标系）
# # 第1帧之后，从第2帧开始，这个值会被不断更新
# current_global_transform = np.eye(4)

# # ----------------------------
# # 4. 逐帧配准后续点云
# # ----------------------------

# # 从第2个文件开始处理（索引为1），输出文件名为 registered_002.ply 起
# for idx, filename in enumerate(all_files[1:], start=2):
#     # 构建当前源点云（待配准）的路径
#     source_path = os.path.join(input_folder, filename)
#     print(f"\n--- 正在配准第 {idx} 帧: {filename} ---")

#     # 读取源点云（当前帧）
#     source_legacy = o3d.io.read_point_cloud(source_path)
#     source_legacy.remove_non_finite_points()  # 清理非法点

#     # 读取上一帧的配准结果作为目标（target）
#     # 例如：配准第3帧时，target 是 registered_002.ply
#     target_path = os.path.join(output_dir, f"registered_{idx-1:03d}.ply")
#     target_legacy = o3d.io.read_point_cloud(target_path)
#     target_legacy.remove_non_finite_points()

#     # 对源点云和目标点云进行体素降采样，加速 ICP
#     source_down = source_legacy.voxel_down_sample(voxel_size=voxel_size)
#     target_down = target_legacy.voxel_down_sample(voxel_size=voxel_size)
#     print(f"📊 降采样后点数 - 源: {len(source_down.points)}, 目标: {len(target_down.points)}")

#     # 将降采样后的点云转换为 Open3D Tensor 格式，并移至 GPU（CUDA:0）
#     source_t = o3d.t.geometry.PointCloud.from_legacy(source_down).to(o3d.core.Device("CUDA:0"))
#     target_t = o3d.t.geometry.PointCloud.from_legacy(target_down).to(o3d.core.Device("CUDA:0"))

#     # 执行 GPU 加速的 ICP 配准
#     print("🚀 正在运行 GPU-ICP...")
#     result = o3d.t.pipelines.registration.icp(
#         source=source_t,
#         target=target_t,
#         max_correspondence_distance=max_correspondence_distance,
#         estimation_method=o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
#         criteria=o3d.t.pipelines.registration.ICPConvergenceCriteria(
#             relative_fitness=1e-6,
#             relative_rmse=1e-6,
#             max_iteration=100  # 最大迭代次数
#         )
#     )

#     # 从结果中提取相对变换矩阵（从当前源帧到上一帧配准结果的变换）
#     relative_transform = result.transformation.cpu().numpy()
#     print("🔄 估计的相对变换矩阵:\n", relative_transform)

#     # 更新累计变换：T_global = T_prev_global @ T_relative
#     # 即：当前帧原始坐标系 → 全局坐标系
#     current_global_transform = current_global_transform @ relative_transform

#     # 保存当前帧的全局变换（可选，用于后续分析）
#     global_transforms.append(current_global_transform)

#     # 将原始（未降采样）的源点云应用全局变换，得到其在全局坐标系下的位置
#     source_registered = copy.deepcopy(source_legacy)
#     source_registered.transform(current_global_transform)

#     # 保存当前帧的配准结果
#     output_filename = f"registered_{idx:03d}.ply"
#     current_output_path = os.path.join(output_dir, output_filename)
#     o3d.io.write_point_cloud(current_output_path, source_registered)
#     print(f"✅ 第 {idx} 帧配准完成，已保存为 {current_output_path}")

#     # 将当前配准后的点云合并到最终完整点云中
#     final_combined_pcd += source_registered

# # ----------------------------
# # 5. 保存最终融合的完整点云
# # ----------------------------

# # 构建最终输出路径
# final_output_path = os.path.join(output_dir, "final_registered_full.ply")

# # 写入完整点云文件
# o3d.io.write_point_cloud(final_output_path, final_combined_pcd)

# # 打印完成信息
# print(f"\n🎉 所有点云配准与融合完成！")
# print(f"📁 每帧结果保存在: {output_dir}/registered_*.ply")
# print(f"💾 完整融合点云保存为: {final_output_path}")
# print(f"📈 最终点云包含 {len(final_combined_pcd.points)} 个点")




# -*- coding: utf-8 -*-
"""
点云序列融合脚本
功能：
  1. 读取 input_ply/ 下的 *-pcd.ply 文件（如 1-pcd.ply, 2-pcd.ply...）
  2. 以第1帧为全局参考坐标系
  3. 逐帧配准到全局坐标系
  4. 将所有配准后的点云**融合**为一个完整点云
  5. 保存融合后的完整点云（final_registered_full.ply）
"""

# -*- coding: utf-8 -*-
"""
点云序列融合脚本
功能：
  1. 读取 input_ply/ 下的 *-pcd.ply 文件
  2. 以第1帧为全局参考坐标系
  3. 逐帧配准到全局坐标系
  4. 将所有配准后的点云融合为一个完整点云
  5. 保存融合后的完整点云（final_registered_full.ply）
"""

import os
import numpy as np
import open3d as o3d

# ----------------------------
# 1. 配置路径和参数
# ----------------------------

# 输入文件夹：存放原始点云
input_folder = "../input_ply"

# 输出文件夹：存放融合结果
output_dir = "../output_ply"
os.makedirs(output_dir, exist_ok=True)

# ICP 配准参数
voxel_size = 20.0                      # 体素降采样尺寸
max_correspondence_distance = 100.0    # ICP 最大对应距离

# ----------------------------
# 2. 获取并排序输入文件
# ----------------------------

# 获取所有以 "-pcd.ply" 结尾的文件
all_files = [f for f in os.listdir(input_folder) if f.endswith("-pcd.ply")]

# 按文件名前缀的数字排序（如 "1-pcd.ply" -> 1, "10-pcd.ply" -> 10）
all_files.sort(key=lambda x: int(x.split('-')[0]))

# 检查至少需要2个点云文件
if len(all_files) < 2:
    raise ValueError("输入文件夹中至少需要两个点云文件（如 1-pcd.ply, 2-pcd.ply）！")

print(f"✅ 找到 {len(all_files)} 个点云文件: {all_files}")

# ----------------------------
# 3. 初始化：第1帧作为全局参考
# ----------------------------

# 读取第1帧点云
first_pcd_path = os.path.join(input_folder, all_files[0])
global_target = o3d.io.read_point_cloud(first_pcd_path)
global_target.remove_non_finite_points()  # 移除非法点

# 保存第1帧作为融合的初始结果（关键修正：使用merged_001.ply）
init_output_path = os.path.join(output_dir, "merged_001.ply")
o3d.io.write_point_cloud(init_output_path, global_target)
print(f"✅ 初始化融合: {init_output_path} (第1帧)")

# ----------------------------
# 4. 创建融合点云（初始为第1帧）
# ----------------------------
final_pcd = o3d.geometry.PointCloud()
final_pcd.points = o3d.utility.Vector3dVector(np.asarray(global_target.points))
final_pcd.colors = o3d.utility.Vector3dVector(np.asarray(global_target.colors))
print(f"✅ 融合初始化: 包含第1帧 ({len(final_pcd.points)} points)")

# ----------------------------
# 5. 逐帧配准并融合
# ----------------------------
for idx, filename in enumerate(all_files[1:], start=2):
    print(f"\n--- 配准并融合第 {idx} 帧: {filename} ---")
    
    # 读取当前帧点云
    source_path = os.path.join(input_folder, filename)
    source_pcd = o3d.io.read_point_cloud(source_path)
    source_pcd.remove_non_finite_points()
    
    # 读取上一帧的融合结果（作为目标）
    # 修正：使用 merged_{idx-1:03d}.ply，如第2帧读取 merged_001.ply
    target_path = os.path.join(output_dir, f"merged_{idx-1:03d}.ply")
    target_pcd = o3d.io.read_point_cloud(target_path)
    target_pcd.remove_non_finite_points()

    # 体素降采样加速
    source_down = source_pcd.voxel_down_sample(voxel_size=voxel_size)
    target_down = target_pcd.voxel_down_sample(voxel_size=voxel_size)
    
    # GPU ICP 配准（关键修正：使用正确的设备指定）
    source_t = o3d.t.geometry.PointCloud.from_legacy(source_down).to(o3d.core.Device("CUDA:0"))
    target_t = o3d.t.geometry.PointCloud.from_legacy(target_down).to(o3d.core.Device("CUDA:0"))
    
    result = o3d.t.pipelines.registration.icp(
        source=source_t,
        target=target_t,
        max_correspondence_distance=max_correspondence_distance,
        estimation_method=o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
        criteria=o3d.t.pipelines.registration.ICPConvergenceCriteria(
            relative_fitness=1e-6,
            relative_rmse=1e-6,
            max_iteration=100
        )
    )
    
    # 获取变换矩阵
    transform = result.transformation.cpu().numpy()
    
    # 应用变换到原始点云（非降采样）
    source_pcd.transform(transform)
    
    # 融合到最终点云
    final_pcd.points.extend(o3d.utility.Vector3dVector(np.asarray(source_pcd.points)))
    final_pcd.colors.extend(o3d.utility.Vector3dVector(np.asarray(source_pcd.colors)))
    
    # 保存当前融合结果
    merged_path = os.path.join(output_dir, f"merged_{idx:03d}.ply")
    o3d.io.write_point_cloud(merged_path, final_pcd)
    print(f"✅ 融合完成: {merged_path} (总点数: {len(final_pcd.points)})")

# ----------------------------
# 6. 保存最终融合点云
# ----------------------------
final_output_path = os.path.join(output_dir, "final_registered_full.ply")
o3d.io.write_point_cloud(final_output_path, final_pcd)
print(f"\n🎉 点云融合完成!")
print(f"📁 最终融合点云: {final_output_path}")
print(f"📈 总点数: {len(final_pcd.points)}")