# 导入所需的标准库模块
import os              # 用于操作系统相关操作（如路径、环境变量）
import shutil          # 用于高级文件操作（如复制、删除）
import subprocess      # 用于调用外部命令或脚本（如运行 run.sh）
import time            # 用于时间控制（如 sleep）
from pathlib import Path  # 面向对象的路径操作工具

# === 全局配置区：根据你的实际路径修改 ===
DIR_A = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test/temp_test_images"
# ↑ 输入目录：新图片不断加入此文件夹

WORK_DIR = "/home/zqdl_ai2060/zy_account/AdelaiDepth-main/LeReS/Minist_Test"
# ↑ 算法工作目录

ALGO_INPUT = os.path.join(WORK_DIR, "test_images")
# ↑ 算法读取图片的目录（每次只放一张）

RUN_SCRIPT = "/home/zqdl_ai2060/zy_account/model_3d/model_examples/AdelaiDepth-main/run.sh"
# ↑ 点云生成脚本路径

PROCESSED_LOG = "/home/zqdl_ai2060/zy_account/model_3d/Point_cloud_registration/probreg/log/run_processed.txt"
# ↑ 已处理图片的日志文件：每行一个文件名，用于判断是否已处理

IMAGE_EXTS = {'.jpg', '.jpeg', '.png'}
# ↑ 支持的图片扩展名（小写）


def load_processed_set():
    """
    从 PROCESSED_LOG 文件中加载所有已处理的文件名，返回一个 set 用于快速查找。
    如果日志文件不存在，则返回空集合。
    """
    processed = set()
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG, 'r') as f:
            for line in f:
                filename = line.strip()
                if filename:  # 忽略空行
                    processed.add(filename)
    return processed


def get_all_images_sorted():
    """
    获取 DIR_A 中所有支持格式的图片，并按文件修改时间升序排序（最早在前）。
    """
    images = []
    for f in Path(DIR_A).iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
            images.append(f)
    # 按修改时间排序：确保从最早加入的图片开始处理
    images.sort(key=lambda x: x.stat().st_mtime)
    return images


def get_next_unprocessed_image():
    """
    从 DIR_A 中找出**第一个尚未处理的图片**（按时间顺序）。
    如果全部已处理或无图片，返回 None。
    """
    processed_set = load_processed_set()
    all_images = get_all_images_sorted()
    
    for img_path in all_images:
        if img_path.name not in processed_set:
            return img_path  # 返回第一个未处理的图片
    
    return None  # 没有未处理的图片


def run_point_cloud_generation():
    """
    调用 run.sh 执行点云生成。
    """
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
        print("✅ Algorithm finished successfully")


def main():
    """
    主循环：持续检查是否有新图未处理，若有则处理第一张未处理的图。
    """
    # 确保必要目录存在
    Path(ALGO_INPUT).mkdir(exist_ok=True)
    Path(os.path.dirname(PROCESSED_LOG)).mkdir(parents=True, exist_ok=True)

    processed_count = 0

    while True:
        # 获取下一个待处理的图片（按时间顺序的第一个未处理项）
        img_path = get_next_unprocessed_image()
        
        if img_path is None:
            print("⏳ No unprocessed images. Waiting...")
            time.sleep(3)
            continue

        print(f"\n📄 Processing: {img_path.name}")

        # 清空算法输入目录（确保干净）
        for f in Path(ALGO_INPUT).iterdir():
            if f.is_file():
                f.unlink()

        # 复制图片到算法输入目录
        shutil.copy2(img_path, os.path.join(ALGO_INPUT, img_path.name))
        print(f"➡️ Copied to {ALGO_INPUT}")

        # 执行点云生成
        try:
            run_point_cloud_generation()
        except Exception as e:
            print(f"💥 Error: {e}")
            # 注意：即使失败，也**不记录为已处理**，下次会重试
            # 如果你希望失败后跳过，可在此处写入日志
            time.sleep(1)
            continue  # 跳过记录，下轮重试

        # 【成功后】才清空输入目录（保险）
        for f in Path(ALGO_INPUT).iterdir():
            if f.is_file():
                f.unlink()

        # 成功处理后，将文件名追加到日志（标记为已处理）
        with open(PROCESSED_LOG, 'a') as f:
            f.write(img_path.name + '\n')
        
        processed_count += 1
        print(f"✅ Finished {img_path.name} ({processed_count} total)")


if __name__ == "__main__":
    main()