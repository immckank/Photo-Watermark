import argparse
import os
from watermark import add_watermark_to_directory

def main():
    """
    主函数，用于解析命令行参数并启动水印添加过程。
    """
    parser = argparse.ArgumentParser(
        description="给图片批量添加拍摄日期水印。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )
    
    parser.add_argument("path", help="图片文件所在的目录路径。")
    parser.add_argument(
        "--font_size", 
        type=int, 
        default=36, 
        help="水印字体大小，默认为 36。"
    )
    parser.add_argument(
        "--color", 
        default="white", 
        help="水印颜色 (例如 'white', 'black', '#FF0000')，默认为白色。"
    )
    parser.add_argument(
        "--position", 
        default="bottom_right", 
        choices=["top_left", "top_right", "bottom_left", "bottom_right", "center"],
        help="水印位置，默认为右下角。"
    )

    args = parser.parse_args()

    # 检查输入路径是否为有效目录
    if not os.path.isdir(args.path):
        print(f"错误：提供的路径 '{args.path}' 不是一个有效的目录。")
        return

    # 调用核心水印处理函数
    add_watermark_to_directory(
        source_dir=args.path,
        font_size=args.font_size,
        color=args.color,
        position=args.position
    )

if __name__ == "__main__":
    main()