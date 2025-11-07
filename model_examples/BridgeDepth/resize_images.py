# resize_images.py
import os
import cv2
import argparse

def resize_images(input_left, input_right, output_left, output_right, size):
    # 创建输出目录
    os.makedirs(output_left, exist_ok=True)
    os.makedirs(output_right, exist_ok=True)

    # 获取所有图片文件（支持 .png 和 .jpg）
    left_images = sorted([f for f in os.listdir(input_left) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    right_images = sorted([f for f in os.listdir(input_right) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    assert len(left_images) == len(right_images), "左右图像数量不一致！"

    for i, (lf, rf) in enumerate(zip(left_images, right_images)):
        print(f"[{i+1}/{len(left_images)}] 处理: {lf}, {rf}")

        # 读取图像
        img_l = cv2.imread(os.path.join(input_left, lf))
        img_r = cv2.imread(os.path.join(input_right, rf))

        if img_l is None or img_r is None:
            print(f"⚠️ 跳过无效图像: {lf}, {rf}")
            continue

        # 缩放
        resized_l = cv2.resize(img_l, size, interpolation=cv2.INTER_LINEAR)
        resized_r = cv2.resize(img_r, size, interpolation=cv2.INTER_LINEAR)

        # 保存
        cv2.imwrite(os.path.join(output_left, lf), resized_l)
        cv2.imwrite(os.path.join(output_right, rf), resized_r)

    print("✅ 图像缩放完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--left", default="./assets/input_images/left_images/")
    parser.add_argument("--right", default="./assets/input_images/right_images/")
    parser.add_argument("--out_left", default="./assets/input_images/left_images_512x384/")
    parser.add_argument("--out_right", default="./assets/input_images/right_images_512x384/")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=384)
    args = parser.parse_args()

    resize_images(
        args.left,
        args.right,
        args.out_left,
        args.out_right,
        (args.width, args.height)
    )