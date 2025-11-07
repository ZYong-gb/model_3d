# -*- coding: utf-8 -*-
"""
点云配准与融合脚本（适用于房间级扫描数据，单位：米）
流程：
  1. 加载 source 和 target 点云
  2. 自动分析点云尺度，设置合理的体素大小
  3. 使用 CPD 进行粗配准（刚体变换）
  4. 使用 Open3D GPU-ICP 进行精细优化
  5. 将配准后的 source 与原始 target 融合为一个点云
  6. 保存：配准结果、原始 target、融合点云
"""

import numpy as np
import open3d as o3d
import transforms3d as t3d
from probreg import cpd
import copy
import os

# ----------------------------
# 1. 配置路径（请根据实际情况修改）
# ----------------------------

SOURCE_PATH = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/1-pcd.ply"
TARGET_PATH = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/2-pcd.ply"

OUTPUT_DIR = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 输出文件名
REGISTERED_SOURCE_PATH = os.path.join(OUTPUT_DIR, "CPD_ICP_Moge_source_registered_cpd_icp.ply")
TARGET_COPY_PATH       = os.path.join(OUTPUT_DIR, "CPD_ICP_Moge_target_original.ply")
MERGED_OUTPUT_PATH     = os.path.join(OUTPUT_DIR, "CPD_ICP_Moge_merged_source_and_target.ply")

# 是否启用 GPU（CuPy + Open3D GPU ICP）
USE_CUDA = True

# ICP 参数
ICP_MAX_DISTANCE = 0.1  # 最大对应距离（米），建议 0.05~0.2（5~20 厘米）

# ----------------------------
# 2. GPU/CPU 设置
# ----------------------------

if USE_CUDA:
    try:
        import cupy as cp
        TO_CPU = cp.asnumpy
        print("✅ 启用 GPU (CuPy) 加速")
    except ImportError:
        print("⚠️ CuPy 未安装，回退到 CPU 模式")
        USE_CUDA = False

if not USE_CUDA:
    cp = np
    TO_CPU = lambda x: x
    print("💻 使用 CPU 计算")

# ----------------------------
# 3. 加载原始点云
# ----------------------------

print("📥 正在加载原始点云...")
if not os.path.exists(SOURCE_PATH) or not os.path.exists(TARGET_PATH):
    raise FileNotFoundError(f"点云文件不存在！请检查路径：\n{SOURCE_PATH}\n{TARGET_PATH}")

source_full = o3d.io.read_point_cloud(SOURCE_PATH)
target_full = o3d.io.read_point_cloud(TARGET_PATH)

source_full.remove_non_finite_points()
target_full.remove_non_finite_points()

# 🔑 关键修复：假设原始数据是毫米，转换为米
print("🔧 将点云从毫米转换为米...")
source_full.points = o3d.utility.Vector3dVector(np.asarray(source_full.points) / 1000.0)
target_full.points = o3d.utility.Vector3dVector(np.asarray(target_full.points) / 1000.0)

print(f"📊 原始点数 - Source: {len(source_full.points):,}, Target: {len(target_full.points):,}")

# 保存原始 target（用于融合和对比）
o3d.io.write_point_cloud(TARGET_COPY_PATH, target_full)
print(f"💾 原始 target 已保存: {TARGET_COPY_PATH}")

# ----------------------------
# 4. 分析点云尺度，自动设置 voxel_size
# ----------------------------

def estimate_voxel_size(pcd, target_points=5000):
    """根据点云范围估算合适的体素尺寸，目标点数约 target_points"""
    bbox = pcd.get_axis_aligned_bounding_box()
    diag = np.linalg.norm(bbox.max_bound - bbox.min_bound)
    if diag == 0:
        return 0.01
    # voxel ≈ 对角线长度 / (目标点数)^(1/3)
    voxel = diag / (target_points ** (1/3))
    return max(voxel, 0.005)  # 至少 5mm

# 打印边界框（调试用）
bbox_s = source_full.get_axis_aligned_bounding_box()
bbox_t = target_full.get_axis_aligned_bounding_box()
print(f"📏 Source 范围: min={bbox_s.min_bound}, max={bbox_s.max_bound}")
print(f"📏 Target 范围: min={bbox_t.min_bound}, max={bbox_t.max_bound}")

VOXEL_SIZE_COARSE = estimate_voxel_size(source_full, target_points=5000)
print(f"🎯 自动设置 CPD 降采样体素尺寸: {VOXEL_SIZE_COARSE:.4f} m")

# ----------------------------
# 5. 降采样用于 CPD 粗配准
# ----------------------------

print(f"🪓 对点云进行体素降采样 (voxel_size={VOXEL_SIZE_COARSE:.4f} m) 用于 CPD...")

source_coarse = source_full.voxel_down_sample(voxel_size=VOXEL_SIZE_COARSE)
target_coarse = target_full.voxel_down_sample(voxel_size=VOXEL_SIZE_COARSE)

# 强制限制点数（防极端情况）
MAX_POINTS_FOR_CPD = 10000
if len(source_coarse.points) > MAX_POINTS_FOR_CPD:
    indices = np.random.choice(len(source_coarse.points), MAX_POINTS_FOR_CPD, replace=False)
    source_coarse = source_coarse.select_by_index(indices)
if len(target_coarse.points) > MAX_POINTS_FOR_CPD:
    indices = np.random.choice(len(target_coarse.points), MAX_POINTS_FOR_CPD, replace=False)
    target_coarse = target_coarse.select_by_index(indices)

source_np = np.asarray(source_coarse.points, dtype=np.float32)
target_np = np.asarray(target_coarse.points, dtype=np.float32)

print(f"📊 降采样后点数 - Source: {source_np.shape[0]:,}, Target: {target_np.shape[0]:,}")

source_gpu = cp.asarray(source_np) if USE_CUDA else source_np
target_gpu = cp.asarray(target_np) if USE_CUDA else target_np

# ----------------------------
# 6. CPD 粗配准（刚体，无缩放）
# ----------------------------

print("🔄 执行 Rigid CPD 粗配准...")
rcpd = cpd.RigidCPD(source=source_gpu, use_cuda=USE_CUDA, update_scale=False)
tf_param, _, _ = rcpd.registration(target_gpu)

rot = TO_CPU(tf_param.rot)
t = TO_CPU(tf_param.t)

euler_deg = np.rad2deg(t3d.euler.mat2euler(rot))
print(f"\n✅ CPD 粗配准结果:")
print(f"  旋转 (ZYX, 度): [{euler_deg[0]:.2f}, {euler_deg[1]:.2f}, {euler_deg[2]:.2f}]")
print(f"  平移 (m): [{t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f}]")

T_cpd = np.eye(4)
T_cpd[:3, :3] = rot
T_cpd[:3, 3] = t

# ----------------------------
# 7. 应用 CPD 变换到原始 source
# ----------------------------

source_after_cpd = copy.deepcopy(source_full)
source_after_cpd.transform(T_cpd)

# ----------------------------
# 8. GPU-ICP 精细配准（使用原始高密度点云）
# ----------------------------

print("🔍 执行 GPU-ICP 精细配准...")

# 注意：Open3D Tensor ICP 需要点云转为 tensor 格式
source_tensor = o3d.t.geometry.PointCloud.from_legacy(source_after_cpd)
target_tensor = o3d.t.geometry.PointCloud.from_legacy(target_full)  # 使用原始 target 提高精度

result_icp = o3d.t.pipelines.registration.icp(
    source=source_tensor,
    target=target_tensor,
    max_correspondence_distance=ICP_MAX_DISTANCE,
    estimation_method=o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
    criteria=o3d.t.pipelines.registration.ICPConvergenceCriteria(max_iteration=50)
)

T_icp = result_icp.transformation.cpu().numpy()
print(f"✅ ICP 精细配准完成:")
print(f"   Fitness (重合率): {result_icp.fitness:.4f}")
print(f"   Inlier RMSE      : {result_icp.inlier_rmse:.4f} m")

# 合并变换：先 CPD，再 ICP → T_total = T_icp @ T_cpd
T_total = T_icp @ T_cpd

# ----------------------------
# 9. 应用最终变换并融合点云
# ----------------------------

print("💾 应用最终变换并生成融合点云...")

# 配准后的 source（高密度）
source_final = copy.deepcopy(source_full)
source_final.transform(T_total)

# 保存配准后的 source
o3d.io.write_point_cloud(REGISTERED_SOURCE_PATH, source_final)
print(f"✅ 配准后的 source 已保存: {REGISTERED_SOURCE_PATH}")

# 👇 关键步骤：融合两个点云（配准后的 source + 原始 target）
merged_pcd = source_final + target_full

# （可选）轻度去重（避免完全重合的点）
# merged_pcd = merged_pcd.voxel_down_sample(voxel_size=0.005)

# 保存融合结果
o3d.io.write_point_cloud(MERGED_OUTPUT_PATH, merged_pcd)
print(f"🎉 融合点云已保存: {MERGED_OUTPUT_PATH}")
print(f"📈 融合后总点数: {len(merged_pcd.points):,}")

# ----------------------------
# 10. （可选）可视化结果
# ----------------------------

VISUALIZE = False
if VISUALIZE:
    print("\n👁️  显示融合结果（红: 配准后 source, 蓝: target）...")
    vis_source = copy.deepcopy(source_final)
    vis_target = copy.deepcopy(target_full)
    vis_source.paint_uniform_color([1, 0, 0])  # 红色
    vis_target.paint_uniform_color([0, 0, 1])  # 蓝色
    o3d.visualization.draw_geometries([vis_target, vis_source],
                                        window_name="配准与融合结果")