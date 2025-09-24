# watermark.py
# -*- coding: utf-8 -*-

import os
import argparse
# 新增导入 ImageOps 模块
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageOps

# --- vibe coding style: keep it simple, functional, and clear ---

# EXIF 'DateTimeOriginal' 标签的数字代码，这是照片的拍摄时间
DATETIME_ORIGINAL_TAG = 36867

def get_exif_date(img_path):
    """
    从图片文件中获取拍摄日期（YYYY-MM-DD）。
    如果找不到 EXIF 信息或日期标签，则返回 None。
    """
    try:
        img = Image.open(img_path)
        exif_data = img._getexif()

        if exif_data and DATETIME_ORIGINAL_TAG in exif_data:
            # EXIF 日期格式通常是 'YYYY:MM:DD HH:MM:SS'
            date_str = exif_data[DATETIME_ORIGINAL_TAG]
            # 我们只需要年月日部分，并替换冒号为连字符
            return date_str.split(' ')[0].replace(':', '-')
    except (AttributeError, KeyError, IndexError, IOError):
        # 发生任何错误（如无EXIF数据、文件损坏等），都静默处理
        print(f"警告: 无法读取 '{os.path.basename(img_path)}' 的 EXIF 日期。")
    return None

def add_watermark(image_path, output_path, text, font_path, font_size, color, position):
    """
    为单个图片添加文本水印。
    """
    try:
        with Image.open(image_path) as original_image:
            # ================================================================= #
            # === 这里是关键的修正 ===
            # 使用 ImageOps.exif_transpose 来根据 EXIF 信息自动旋转/翻转图片
            base = ImageOps.exif_transpose(original_image)
            # ================================================================= #
            
            # 转换为 RGBA 以支持透明水印
            base = base.convert("RGBA")

            # 创建一个透明的图层用于绘制文本
            txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))

            # 加载字体
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                print(f"错误: 找不到字体文件 '{font_path}'。将使用默认字体。")
                font = ImageFont.load_default()

            d = ImageDraw.Draw(txt_layer)
            img_width, img_height = base.size
            
            # 使用 textbbox 获取更精确的文本尺寸
            text_bbox = d.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # --- 根据用户选择计算水印位置 ---
            margin = 20 # 水印与图片边缘的距离
            x, y = 0, 0

            if position == 'top-left':
                x, y = margin, margin
            elif position == 'top-right':
                x, y = img_width - text_width - margin, margin
            elif position == 'bottom-left':
                x, y = margin, img_height - text_height - margin
            elif position == 'bottom-right':
                x, y = img_width - text_width - margin, img_height - text_height - margin
            elif position == 'center':
                x = (img_width - text_width) / 2
                y = (img_height - text_height) / 2

            # 在透明图层上绘制文本
            d.text((x, y), text, font=font, fill=color)

            # 将文本图层合并到原始图片上
            out = Image.alpha_composite(base, txt_layer)
            
            # 转换为 RGB 格式以便保存为 JPG
            out = out.convert("RGB")
            out.save(output_path, "JPEG", quality=95)
            print(f"成功: '{os.path.basename(image_path)}' -> '{os.path.basename(output_path)}'")

    except Exception as e:
        print(f"错误: 处理 '{os.path.basename(image_path)}' 时失败: {e}")

def main():
    """主函数，负责解析命令行参数和处理文件。"""
    parser = argparse.ArgumentParser(
        description="给图片批量添加拍摄日期水印。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )
    parser.add_argument("input_path", type=str, help="包含图片的目录路径。")
    parser.add_argument(
        "--font_size", 
        type=int, 
        default=50, 
        help="水印字体大小 (默认: 50)"
    )
    parser.add_argument(
        "--color", 
        type=str, 
        default="rgba(255, 255, 255, 180)", 
        help="水印颜色 (例如 'white', '#FFFFFF', 'rgba(255, 255, 255, 180)')\n(默认: 'rgba(255, 255, 255, 180)')"
    )
    parser.add_argument(
        "--position", 
        type=str, 
        default="bottom-right", 
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        help="水印位置 (默认: bottom-right)"
    )
    parser.add_argument(
        "--font", 
        dest="font_path", 
        type=str, 
        default="Roboto-Regular.ttf", 
        help="字体文件的路径 (例如 'C:/Windows/Fonts/Arial.ttf')\n(默认: Roboto-Regular.ttf, 请确保它在脚本同目录)"
    )

    args = parser.parse_args()

    # --- 检查输入路径是否存在且为目录 ---
    if not os.path.isdir(args.input_path):
        print(f"错误: 输入路径 '{args.input_path}' 不是一个有效的目录。")
        return

    # --- 创建输出目录 ---
    base_dir_name = os.path.basename(os.path.normpath(args.input_path))
    output_dir = os.path.join(args.input_path, f"{base_dir_name}_watermark")
    os.makedirs(output_dir, exist_ok=True)
    print(f"水印图片将保存在: {output_dir}")

    # --- 遍历目录中的所有文件 ---
    supported_formats = ('.jpg', '.jpeg', '.tiff', '.tif')
    for filename in os.listdir(args.input_path):
        if filename.lower().endswith(supported_formats):
            image_full_path = os.path.join(args.input_path, filename)
            
            # 获取EXIF日期
            date_text = get_exif_date(image_full_path)
            
            if date_text:
                # 构建输出文件路径
                output_full_path = os.path.join(output_dir, filename)
                # 添加水印
                add_watermark(
                    image_full_path, 
                    output_full_path, 
                    date_text, 
                    args.font_path, 
                    args.font_size, 
                    args.color, 
                    args.position
                )

    print("\n处理完成！")

if __name__ == '__main__':
    main()