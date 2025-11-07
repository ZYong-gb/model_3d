import numpy as np
import open3d as o3d
import time

# ==============================
# 配置是否使用 CUDA（GPU加速）
# ==============================
use_cuda = True

if use_cuda:
    import cupy as cp
    # 将 CuPy 数组转为 NumPy（用于保存或打印）
    to_cpu = cp.asnumpy
    # 设置内存池以提高 GPU 内存分配效率
    cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
else:
    # 若不使用 GPU，则用 NumPy 替代 CuPy
    cp = np
    to_cpu = lambda x: x

# 导入 probreg 的 AffineCPD 算法
from probreg import cpd


# ==============================
# 工具函数：加载 .ply 点云
# ==============================
def load_point_cloud_ply(filename):
    """
    从 .ply 文件加载点云坐标。
    
    参数:
        filename (str): .ply 文件路径
    
    返回:
        np.ndarray: 形状为 (N, 3) 的点坐标数组
    """
    pcd = o3d.io.read_point_cloud(filename)
    if pcd.is_empty():
        raise ValueError(f"无法加载点云文件: {filename}")
    return np.asarray(pcd.points, dtype=np.float32)


# ==============================
# 工具函数：保存点云为 .ply 文件
# ==============================
def save_point_cloud_ply(points, filename):
    """
    将点坐标保存为 .ply 文件。
    
    参数:
        points (np.ndarray): 形状为 (N, 3) 的点坐标
        filename (str): 保存路径
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(filename, pcd, write_ascii=False)


# ——————————————————————————————
# 设置输入输出文件路径
# ——————————————————————————————
source_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/1-pcd.ply"
target_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/input_ply/2-pcd.ply"

# 输出文件路径
registered_source_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/Affine_CPD_Moge_registered_source.ply"
combined_file = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/output_ply/Affine_CPD_Moge_combined.ply"

# ——————————————————————————————
# 步骤1: 加载点云（CPU 上的 NumPy 数组）
# ——————————————————————————————
print("正在加载点云...")
source_np = load_point_cloud_ply(source_file)  # shape: (N, 3)
target_np = load_point_cloud_ply(target_file)  # shape: (M, 3)
print(f"Source 点数: {source_np.shape[0]}, Target 点数: {target_np.shape[0]}")

# ——————————————————————————————
# 步骤2: 将数据转移到 GPU（如果启用 CUDA）
# ——————————————————————————————
print("正在准备 GPU 数据..." if use_cuda else "使用 CPU 计算...")
source_gpu = cp.asarray(source_np, dtype=cp.float32)
target_gpu = cp.asarray(target_np, dtype=cp.float32)

# ——————————————————————————————
# 步骤3: 执行 AffineCPD 配准
# ——————————————————————————————
print("开始 AffineCPD 配准...")
acpd = cpd.AffineCPD(source_gpu, use_cuda=use_cuda)

start_time = time.time()
tf_param, _, _ = acpd.registration(target_gpu)
elapsed_time = time.time() - start_time

print(f"配准完成！耗时: {elapsed_time:.3f} 秒")
print("仿射变换矩阵 B:\n", to_cpu(tf_param.b))
print("平移向量 t:", to_cpu(tf_param.t))

# ——————————————————————————————
# 步骤4: 应用变换，得到对齐后的 source
# ——————————————————————————————
source_transformed_gpu = tf_param.transform(source_gpu)
source_transformed_np = to_cpu(source_transformed_gpu)  # 转回 CPU

# 保存配准后的 source
save_point_cloud_ply(source_transformed_np, registered_source_file)
print(f"配准后的 Source 已保存至: {registered_source_file}")

# ——————————————————————————————
# 步骤5: 融合配准后的 source 与原始 target
# ——————————————————————————————
print("正在融合点云...")
combined_points = np.vstack([source_transformed_np, target_np])  # 垂直拼接 (N+M, 3)

# 保存融合后的点云
save_point_cloud_ply(combined_points, combined_file)
print(f"融合点云（配准后的 Source + 原始 Target）已保存至: {combined_file}")
print(f"融合后总点数: {combined_points.shape[0]}")