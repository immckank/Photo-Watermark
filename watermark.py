import os
from PIL import Image, ImageDraw, ImageFont

# EXIF 标签中代表“拍摄时间”的 ID
DATETIME_ORIGINAL_TAG = 36867

def get_exif_date(image_path):
    """
    从图片文件的 EXIF 信息中读取原始拍摄日期。
    返回 'YYYY-MM-DD' 格式的字符串，如果失败则返回 None。
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data and DATETIME_ORIGINAL_TAG in exif_data:
            # EXIF 日期格式为 'YYYY:MM:DD HH:MM:SS'
            full_date = exif_data[DATETIME_ORIGINAL_TAG]
            # 提取年月日部分，并将冒号替换为连字符
            return full_date.split(' ')[0].replace(':', '-')
    except (AttributeError, KeyError, IndexError, TypeError):
        # 忽略那些没有 EXIF 信息或日期信息的图片
        return None
    return None

def calculate_position(image_size, text_size, position, margin=20):
    """
    根据用户设置计算水印文本的精确坐标 (x, y)。
    """
    img_width, img_height = image_size
    text_width, text_height = text_size

    if position == "top_left":
        return (margin, margin)
    elif position == "top_right":
        return (img_width - text_width - margin, margin)
    elif position == "bottom_left":
        return (margin, img_height - text_height - margin)
    elif position == "center":
        return ((img_width - text_width) / 2, (img_height - text_height) / 2)
    else:  # 默认 bottom_right
        return (img_width - text_width - margin, img_height - text_height - margin)

def add_watermark_to_directory(source_dir, font_size, color, position):
    """
    遍历指定目录中的所有图片，添加水印并保存到新的子目录。
    """
    # 1. 创建保存水印图片的新目录
    output_dir_name = os.path.basename(os.path.normpath(source_dir)) + "_watermark"
    output_dir = os.path.join(source_dir, output_dir_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"水印图片将保存在: {output_dir}")

    # 2. 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            source_path = os.path.join(source_dir, filename)
            
            # 3. 获取拍摄日期作为水印文本
            watermark_text = get_exif_date(source_path)
            if not watermark_text:
                print(f"警告: 无法从 '{filename}' 读取拍摄日期，已跳过。")
                continue

            # 4. 绘制水印
            try:
                with Image.open(source_path).convert("RGBA") as base_image:
                    # 创建一个与原图同样大小的透明图层用于绘制文字
                    txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
                    
                    # 加载字体 (建议下载一个 ttf 字体文件放到项目目录)
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except IOError:
                        print("警告: 找不到 'arial.ttf' 字体，将使用默认字体。")
                        font = ImageFont.load_default()

                    draw = ImageDraw.Draw(txt_layer)
                    
                    # 获取文本尺寸以便精确定位
                    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]

                    # 计算坐标
                    pos = calculate_position(base_image.size, (text_width, text_height), position)

                    # 在透明图层上绘制白色文本
                    draw.text(pos, watermark_text, font=font, fill=color)

                    # 将文本图层叠加到原始图片上
                    watermarked_image = Image.alpha_composite(base_image, txt_layer)
                    
                    # 5. 保存处理后的图片
                    output_path = os.path.join(output_dir, filename)
                    # 转换为 RGB 以便保存为 JPG
                    watermarked_image.convert("RGB").save(output_path)
                    print(f"成功为 '{filename}' 添加水印。")

            except Exception as e:
                print(f"处理 '{filename}' 时发生错误: {e}")

    print("\n所有图片处理完成！")