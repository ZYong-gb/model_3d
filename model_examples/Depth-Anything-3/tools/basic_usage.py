# 导入必要的库
import glob, os, torch  # glob用于文件搜索，os用于操作系统操作，torch为PyTorch深度学习框架
import numpy as np  # numpy用于数值计算
from PIL import Image  # PIL用于图像处理
import argparse  # argparse用于命令行参数解析
from depth_anything_3.api import DepthAnything3  # Depth Anything V3模型API

def basic_usage():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Run Depth Anything V3 and save per-image results.")
    
    # 添加输入参数：输入图像文件夹路径
    parser.add_argument("--input", "-i", type=str, default="../assets/examples/SOH",
                        help="Path to input image folder (e.g., ../assets/examples/SOH)")
    
    # 添加输出参数：输出目录路径（默认值为"output_da3"）
    parser.add_argument("--output", "-o", type=str, default="../output_da3",
                        help="Output directory to save results (default: ../output_da3)")
    
    # 添加模型路径参数：预训练模型检查点路径
    parser.add_argument("--model_path", "-m", type=str,
                        default="/model/Depth-Anything-3/checkpoints/DA3NESTED-GIANT-LARGE/",
                        help="Path to model checkpoint")
    
    # 解析命令行参数
    args = parser.parse_args()

    # 设置设备：优先使用GPU（CUDA），否则使用CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 从预训练路径加载Depth Anything V3模型
    model = DepthAnything3.from_pretrained(args.model_path)
    # 将模型移动到指定的设备（GPU或CPU）
    model = model.to(device=device)

    # 支持的图像文件扩展名列表（全部转换为小写比较）
    SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp', '.ppm', '.pgm']
    
    # 方法1：使用glob搜索多种格式
    images = []
    for ext in SUPPORTED_EXTENSIONS:
        # 搜索每种扩展名的文件（不区分大小写）
        images.extend(glob.glob(os.path.join(args.input, f"*{ext}")))
        images.extend(glob.glob(os.path.join(args.input, f"*{ext.upper()}")))  # 大写扩展名
    
    # 方法2：或者使用更简洁的方式，先获取所有文件再过滤
    # all_files = glob.glob(os.path.join(args.input, "*"))
    # images = [f for f in all_files 
    #           if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS 
    #           and os.path.isfile(f)]
    
    # 按文件名排序
    images = sorted(images)
    
    # 如果没有找到支持的图像文件，抛出异常
    if not images:
        # 显示目录内容帮助调试
        print(f"目录 '{args.input}' 中的文件:")
        if os.path.exists(args.input):
            for item in os.listdir(args.input):
                item_path = os.path.join(args.input, item)
                if os.path.isfile(item_path):
                    print(f"  {item} (扩展名: {os.path.splitext(item)[1]})")
                else:
                    print(f"  {item}/ (目录)")
        else:
            print(f"目录不存在: {args.input}")
        
        raise ValueError(f"No supported image files found in {args.input}. "
                         f"支持格式: {', '.join(SUPPORTED_EXTENSIONS)}")

    # 打印找到的图像信息
    print(f"Found {len(images)} images:")
    for img in images[:5]:  # 只显示前5个文件信息
        print(f"  {os.path.basename(img)}")
    if len(images) > 5:
        print(f"  ... 还有 {len(images)-5} 个文件")
    
    print("Running inference...")
    # 对图像列表进行批量推理，返回预测结果
    prediction = model.inference(images)

    # 创建输出目录（如果目录已存在则不会报错）
    os.makedirs(args.output, exist_ok=True)

    # 获取每个图像的基本文件名（不包含扩展名）
    image_basenames = [os.path.splitext(os.path.basename(img))[0] for img in images]

    # 遍历每张图像，保存对应的各种输出数据
    for i, basename in enumerate(image_basenames):
        print(f"Saving data for image: {basename}")

        # 1. 保存RGB图像
        # 获取预处理后的RGB图像
        rgb_img = prediction.processed_images[i]
        # 将numpy数组转换为PIL图像并保存为PNG格式
        Image.fromarray(rgb_img).save(os.path.join(args.output, f"{basename}_rgb.png"))

        # 2. 保存深度图
        # 获取深度数据
        depth = prediction.depth[i]
        # 保存原始深度数据为.npy二进制文件
        np.save(os.path.join(args.output, f"{basename}_depth.npy"), depth)
        # 对深度图进行归一化处理，缩放到0-255范围用于可视化
        depth_vis = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8) * 255
        # 保存深度可视化图像
        Image.fromarray(depth_vis.astype(np.uint8)).save(
            os.path.join(args.output, f"{basename}_depth_vis.png")
        )

        # 3. 保存置信度图
        # 获取置信度数据
        conf = prediction.conf[i]
        # 保存原始置信度数据为.npy文件
        np.save(os.path.join(args.output, f"{basename}_conf.npy"), conf)
        # 将置信度（0-1范围）转换为0-255的灰度图像
        conf_vis = (conf * 255).clip(0, 255).astype(np.uint8)
        # 保存置信度可视化图像
        Image.fromarray(conf_vis).save(
            os.path.join(args.output, f"{basename}_conf_vis.png")
        )

        # 4. 保存相机内参和外参
        # 获取相机内参矩阵K（3x3）
        K = prediction.intrinsics[i]
        # 获取世界坐标系到相机坐标系的变换矩阵W2C（4x4）
        W2C = prediction.extrinsics[i]
        # 保存内参和外参为.npy二进制文件
        np.save(os.path.join(args.output, f"{basename}_K.npy"), K)
        np.save(os.path.join(args.output, f"{basename}_W2C.npy"), W2C)
        # 同时保存为.txt文本文件，便于人工查看（保留6位小数）
        np.savetxt(os.path.join(args.output, f"{basename}_K.txt"), K, fmt="%.6f")
        np.savetxt(os.path.join(args.output, f"{basename}_W2C.txt"), W2C, fmt="%.6f")

    # 所有处理完成，打印输出目录的绝对路径
    print(f"\n✅ All results saved to: {os.path.abspath(args.output)}")

# 脚本入口点
if __name__ == "__main__":
    basic_usage()