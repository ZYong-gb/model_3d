# # 导入所需的标准库模块
# import os
# import shutil
# import subprocess
# import time
# from pathlib import Path
# import copy
# import numpy as np
# import open3d as o3d

# # ============================
# # 全局配置区
# # ============================

# # --- 点云生成相关 ---
# DIR_A = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/temp_test_images"
# WORK_DIR = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test"
# ALGO_INPUT = os.path.join(WORK_DIR, "test_images")
# RUN_SCRIPT = "/home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/run.sh"
# PROCESSED_LOG = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/log/run_processed.txt"
# IMAGE_EXTS = {'.jpg', '.jpeg', '.png'}

# # --- 点云配准相关 ---
# PCD_OUTPUT_DIR = os.path.join(WORK_DIR, "test_images", "outputs")  # run.sh 生成的 .ply 目录
# REGISTERED_OUTPUT_DIR = "../output_ply"  # 配准结果保存目录

# # --- 配准参数 ---
# VOXEL_SIZE = 20.0
# MAX_CORRESPONDENCE_DISTANCE = 100.0

# # ============================
# # 工具函数：点云生成部分
# # ============================

# def load_processed_set():
#     processed = set()
#     if os.path.exists(PROCESSED_LOG):
#         with open(PROCESSED_LOG, 'r') as f:
#             for line in f:
#                 filename = line.strip()
#                 if filename:
#                     processed.add(filename)
#     return processed

# def get_all_images_sorted():
#     images = []
#     for f in Path(DIR_A).iterdir():
#         if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
#             images.append(f)
#     images.sort(key=lambda x: x.stat().st_mtime)
#     return images

# def get_next_unprocessed_image():
#     processed_set = load_processed_set()
#     all_images = get_all_images_sorted()
#     for img_path in all_images:
#         if img_path.name not in processed_set:
#             return img_path
#     return None

# def run_point_cloud_generation():
#     print("🚀 Running point cloud generation...")
#     result = subprocess.run(
#         ["bash", RUN_SCRIPT],
#         cwd=WORK_DIR,
#         capture_output=True,
#         text=True
#     )
#     if result.returncode != 0:
#         print("❌ Algorithm failed!")
#         print("STDERR:", result.stderr)
#         raise RuntimeError("Point cloud generation failed")
#     else:
#         print("✅ Point cloud generation finished successfully")

# # ============================
# # 工具函数：点云配准部分（增量式）
# # ============================

# def incremental_registration(new_pcd_filename):
#     """
#     对新增加的一张点云文件执行增量配准。
#     :param new_pcd_filename: 新增加的点云文件名（形如 '1-pcd.ply'）
#     """
#     os.makedirs(REGISTERED_OUTPUT_DIR, exist_ok=True)

#     # 获取所有已注册的点云文件并排序
#     registered_files = [f for f in os.listdir(REGISTERED_OUTPUT_DIR) if f.endswith(".ply")]
#     registered_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

#     if len(registered_files) == 0:
#         # 如果是第一张点云，则直接复制为 registered_001.ply
#         first_output_path = os.path.join(REGISTERED_OUTPUT_DIR, "registered_001.ply")
#         shutil.copy(os.path.join(PCD_OUTPUT_DIR, new_pcd_filename), first_output_path)
#         print(f"✅ First frame saved as reference: {first_output_path}")
#     else:
#         # 上一帧的配准结果作为 target
#         last_registered_path = os.path.join(REGISTERED_OUTPUT_DIR, registered_files[-1])
#         source_path = os.path.join(PCD_OUTPUT_DIR, new_pcd_filename)

#         source_legacy = o3d.io.read_point_cloud(source_path)
#         target_legacy = o3d.io.read_point_cloud(last_registered_path)
#         source_legacy.remove_non_finite_points()
#         target_legacy.remove_non_finite_points()

#         # 降采样
#         if VOXEL_SIZE > 0:
#             source_down = source_legacy.voxel_down_sample(voxel_size=VOXEL_SIZE)
#             target_down = target_legacy.voxel_down_sample(voxel_size=VOXEL_SIZE)
#         else:
#             source_down = source_legacy
#             target_down = target_legacy

#         print(f"Downsampled - source: {len(source_down.points)}, target: {len(target_down.points)}")

#         # GPU ICP
#         try:
#             source_t = o3d.t.geometry.PointCloud.from_legacy(source_down).to(o3d.core.Device("CUDA:0"))
#             target_t = o3d.t.geometry.PointCloud.from_legacy(target_down).to(o3d.core.Device("CUDA:0"))
#         except Exception as e:
#             print(f"⚠️ CUDA not available, falling back to CPU. Error: {e}")
#             source_t = o3d.t.geometry.PointCloud.from_legacy(source_down)
#             target_t = o3d.t.geometry.PointCloud.from_legacy(target_down)

#         result = o3d.t.pipelines.registration.icp(
#             source_t,
#             target_t,
#             max_correspondence_distance=MAX_CORRESPONDENCE_DISTANCE,
#             estimation_method=o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
#             criteria=o3d.t.pipelines.registration.ICPConvergenceCriteria(
#                 relative_fitness=1e-6,
#                 relative_rmse=1e-6,
#                 max_iteration=100
#             )
#         )

#         transformation = result.transformation.cpu().numpy()
#         print("Estimated transformation:\n", transformation)

#         # 应用变换
#         source_registered = copy.deepcopy(source_legacy)
#         source_registered.transform(transformation)

#         # 保存结果
#         next_idx = len(registered_files) + 1
#         output_path = os.path.join(REGISTERED_OUTPUT_DIR, f"registered_{next_idx:03d}.ply")
#         o3d.io.write_point_cloud(output_path, source_registered)
#         print(f"✅ Frame {next_idx} registered and saved to {output_path}")

# # ============================
# # 主流程
# # ============================

# def main():
#     # 确保必要目录存在
#     Path(ALGO_INPUT).mkdir(exist_ok=True)
#     Path(os.path.dirname(PROCESSED_LOG)).mkdir(parents=True, exist_ok=True)
#     Path(REGISTERED_OUTPUT_DIR).mkdir(exist_ok=True)

#     processed_count = 0

#     while True:
#         img_path = get_next_unprocessed_image()
#         if img_path is None:
#             print("⏳ No unprocessed images. Waiting...")
#             time.sleep(3)
#             continue

#         print(f"\n📄 Processing image: {img_path.name}")

#         # 清空输入目录
#         for f in Path(ALGO_INPUT).iterdir():
#             if f.is_file():
#                 f.unlink()

#         # 复制图片
#         shutil.copy2(img_path, os.path.join(ALGO_INPUT, img_path.name))
#         print(f"➡️ Copied to {ALGO_INPUT}")

#         # 生成点云
#         try:
#             run_point_cloud_generation()
#         except Exception as e:
#             print(f"💥 Point cloud generation failed: {e}")
#             time.sleep(1)
#             continue

#         # 查找新生成的点云文件（假设按数字顺序排列）
#         pcd_files = sorted([f for f in os.listdir(PCD_OUTPUT_DIR) if f.endswith("-pcd.ply")], key=lambda x: int(x.split('-')[0]))
#         if len(pcd_files) > 0:
#             latest_pcd = pcd_files[-1]
#             print(f"🔍 Found new point cloud file: {latest_pcd}")

#             # 执行增量配准
#             try:
#                 incremental_registration(latest_pcd)
#             except Exception as e:
#                 print(f"⚠️ Registration failed (but image is still marked as processed): {e}")
#         else:
#             print("⚠️ No new point cloud file found.")

#         # 标记图片为已处理（即使配准失败也标记，避免重复生成点云）
#         with open(PROCESSED_LOG, 'a') as f:
#             f.write(img_path.name + '\n')

#         processed_count += 1
#         print(f"✅ Finished processing {img_path.name} ({processed_count} total)")

# if __name__ == "__main__":
#     main()







import os
import shutil
import subprocess
import time
from pathlib import Path
import copy
import numpy as np
import open3d as o3d

# ============================
# 全局配置区
# ============================

# --- 点云生成相关 ---
DIR_A = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/temp_test_images"
WORK_DIR = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test"
ALGO_INPUT = os.path.join(WORK_DIR, "test_images")
RUN_SCRIPT = "/home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/run.sh"
PROCESSED_LOG = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/log/run_processed.txt"
IMAGE_EXTS = {'.jpg', '.jpeg', '.png'}

# --- 点云配准与融合相关 ---
PCD_OUTPUT_DIR = os.path.join(WORK_DIR, "test_images", "outputs")
REGISTERED_OUTPUT_DIR = "../output_ply"

# --- 配准参数 ---
VOXEL_SIZE = 20.0
MAX_CORRESPONDENCE_DISTANCE = 100.0

# --- 融合参数 ---
FUSION_VOXEL_SIZE = 10.0  # 融合时降采样体素大小（单位需与点云一致）
MAX_POINTS_BEFORE_DOWNSAMPLE = 500_000  # 超过此点数自动降采样

# ============================
# 全局状态（用于累积融合）
# ============================
global_merged_pcd = None


# ============================
# 工具函数：点云生成部分
# ============================

def load_processed_set():
    processed = set()
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG, 'r') as f:
            for line in f:
                filename = line.strip()
                if filename:
                    processed.add(filename)
    return processed

def get_all_images_sorted():
    images = []
    for f in Path(DIR_A).iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
            images.append(f)
    images.sort(key=lambda x: x.stat().st_mtime)
    return images

def get_next_unprocessed_image():
    processed_set = load_processed_set()
    all_images = get_all_images_sorted()
    for img_path in all_images:
        if img_path.name not in processed_set:
            return img_path
    return None

def run_point_cloud_generation():
    print("🚀 Running point cloud generation...")
    result = subprocess.run(
        ["bash", RUN_SCRIPT],
        cwd=WORK_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ Algorithm failed!")
        print("STDERR:", result.stderr)
        raise RuntimeError("Point cloud generation failed")
    else:
        print("✅ Point cloud generation finished successfully")


# ============================
# 工具函数：增量配准 + 实时融合
# ============================

def incremental_registration_and_fusion(new_pcd_filename):
    global global_merged_pcd
    os.makedirs(REGISTERED_OUTPUT_DIR, exist_ok=True)

    registered_files = [f for f in os.listdir(REGISTERED_OUTPUT_DIR) if f.endswith(".ply") and f.startswith("registered_")]
    registered_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    source_path = os.path.join(PCD_OUTPUT_DIR, new_pcd_filename)

    # 读取当前帧点云
    source_legacy = o3d.io.read_point_cloud(source_path)
    source_legacy.remove_non_finite_points()
    if source_legacy.is_empty():
        print("⚠️ Current point cloud is empty after cleaning. Skipping.")
        return

    if len(registered_files) == 0:
        # 第一帧：直接作为参考
        transformation = np.eye(4)
        source_registered = copy.deepcopy(source_legacy)
        output_path = os.path.join(REGISTERED_OUTPUT_DIR, "registered_001.ply")
        o3d.io.write_point_cloud(output_path, source_registered)
        print(f"✅ First frame saved as reference: {output_path}")
    else:
        # 后续帧：与上一帧配准
        last_registered_path = os.path.join(REGISTERED_OUTPUT_DIR, registered_files[-1])
        target_legacy = o3d.io.read_point_cloud(last_registered_path)
        target_legacy.remove_non_finite_points()

        if target_legacy.is_empty():
            print("⚠️ Target point cloud is empty. Skipping registration.")
            return

        # 降采样用于配准
        source_down = source_legacy.voxel_down_sample(voxel_size=VOXEL_SIZE) if VOXEL_SIZE > 0 else source_legacy
        target_down = target_legacy.voxel_down_sample(voxel_size=VOXEL_SIZE) if VOXEL_SIZE > 0 else target_legacy

        print(f"Downsampled - source: {len(source_down.points)}, target: {len(target_down.points)}")

        # 尝试 GPU ICP
        try:
            source_t = o3d.t.geometry.PointCloud.from_legacy(source_down).to(o3d.core.Device("CUDA:0"))
            target_t = o3d.t.geometry.PointCloud.from_legacy(target_down).to(o3d.core.Device("CUDA:0"))
        except Exception as e:
            print(f"⚠️ CUDA not available, falling back to CPU. Error: {e}")
            source_t = o3d.t.geometry.PointCloud.from_legacy(source_down)
            target_t = o3d.t.geometry.PointCloud.from_legacy(target_down)

        result = o3d.t.pipelines.registration.icp(
            source_t,
            target_t,
            max_correspondence_distance=MAX_CORRESPONDENCE_DISTANCE,
            estimation_method=o3d.t.pipelines.registration.TransformationEstimationPointToPoint(),
            criteria=o3d.t.pipelines.registration.ICPConvergenceCriteria(
                relative_fitness=1e-6,
                relative_rmse=1e-6,
                max_iteration=100
            )
        )

        transformation = result.transformation.cpu().numpy()
        print("Estimated transformation:\n", transformation)

        # 应用变换到原始（未降采样）点云
        source_registered = copy.deepcopy(source_legacy)
        source_registered.transform(transformation)

        # 保存单帧配准结果
        next_idx = len(registered_files) + 1
        output_path = os.path.join(REGISTERED_OUTPUT_DIR, f"registered_{next_idx:03d}.ply")
        o3d.io.write_point_cloud(output_path, source_registered)
        print(f"✅ Frame {next_idx} registered and saved to {output_path}")

    # ============================
    # 🔥 实时累积融合（核心新增）
    # ============================
    if global_merged_pcd is None:
        global_merged_pcd = copy.deepcopy(source_registered)
    else:
        global_merged_pcd += source_registered  # Open3D 支持 + 合并

    # 自动降采样防止内存爆炸
    if len(global_merged_pcd.points) > MAX_POINTS_BEFORE_DOWNSAMPLE:
        print(f"MemoryWarning Merged point cloud has {len(global_merged_pcd.points)} points. Downsampling...")
        global_merged_pcd = global_merged_pcd.voxel_down_sample(voxel_size=FUSION_VOXEL_SIZE)

    # 保存完整场景
    full_scene_path = os.path.join(REGISTERED_OUTPUT_DIR, "full_scene.ply")
    o3d.io.write_point_cloud(full_scene_path, global_merged_pcd)
    print(f"💾 Full scene updated: {full_scene_path} ({len(global_merged_pcd.points)} points)")


# ============================
# 主流程
# ============================

def main():
    global global_merged_pcd
    Path(ALGO_INPUT).mkdir(exist_ok=True)
    Path(os.path.dirname(PROCESSED_LOG)).mkdir(parents=True, exist_ok=True)
    Path(REGISTERED_OUTPUT_DIR).mkdir(exist_ok=True)

    processed_count = 0

    while True:
        img_path = get_next_unprocessed_image()
        if img_path is None:
            print("⏳ No unprocessed images. Waiting...")
            time.sleep(3)
            continue

        print(f"\n📄 Processing image: {img_path.name}")

        # 清空输入目录
        for f in Path(ALGO_INPUT).iterdir():
            if f.is_file():
                f.unlink()

        shutil.copy2(img_path, os.path.join(ALGO_INPUT, img_path.name))
        print(f"➡️ Copied to {ALGO_INPUT}")

        try:
            run_point_cloud_generation()
        except Exception as e:
            print(f"💥 Point cloud generation failed: {e}")
            time.sleep(1)
            continue

        pcd_files = sorted(
            [f for f in os.listdir(PCD_OUTPUT_DIR) if f.endswith("-pcd.ply")],
            key=lambda x: int(x.split('-')[0])
        )
        if pcd_files:
            latest_pcd = pcd_files[-1]
            print(f"🔍 Found new point cloud file: {latest_pcd}")
            try:
                incremental_registration_and_fusion(latest_pcd)
            except Exception as e:
                print(f"⚠️ Registration or fusion failed: {e}")
        else:
            print("⚠️ No new point cloud file found.")

        # 标记为已处理
        with open(PROCESSED_LOG, 'a') as f:
            f.write(img_path.name + '\n')

        processed_count += 1
        print(f"✅ Finished processing {img_path.name} ({processed_count} total)")


if __name__ == "__main__":
    main()