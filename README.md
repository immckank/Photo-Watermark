# Photo-Watermark

Large Language Model Assisted Software Engineering '25, Assignment 1

这是一个简单而强大的 Python 命令行工具，它可以批量读取照片的 EXIF 信息中的拍摄日期，并将其作为水印添加到图片上。它不会修改您的原始照片，而是将处理后的图片保存在一个新的子目录中。

![示例图片](./my_images/my_images_watermark/IMG_1176.JPG)
*(这是一个示例效果图)*

## ✨ 主要功能

- **自动读取 EXIF**：自动从图片元数据中提取拍摄日期（格式：`YYYY-MM-DD`）作为水印内容。
- **批量处理**：一次性处理指定文件夹内的所有支持的图片文件 (`.jpg`, `.jpeg`, `.tiff`)。
- **高度自定义**：自由调整水印的字体、大小、颜色和位置。
- **智能方向校正**：自动处理因 EXIF 方向信息导致的图片旋转问题，确保输出图片方向正确。
- **安全无损**：绝不覆盖原始文件，带水印的图片会保存在新建的子目录中。

## 🚀 开始使用

### 1. 环境准备

在使用脚本之前，您需要准备好以下环境：

- **Python 3**: 请确保您的电脑上安装了 Python 3。
- **Pillow 库**: 这是处理图片所必需的 Python 库。如果尚未安装，请打开终端或命令行并运行：
  ```bash
  pip install Pillow
  ```
- **字体文件**: 您需要一个 `.ttf` 或 `.otf` 格式的字体文件来生成水印。
  - 推荐从 [Google Fonts](https://fonts.google.com/specimen/Roboto) 下载免费的 `Roboto` 字体。
  - 下载后，将 `Roboto-Regular.ttf` 文件放在与 `watermark.py` 脚本相同的目录下。

### 2. 文件结构

为了让脚本顺利运行，请按下图所示组织您的文件：

```
project_directory/
├── watermark.py           # 脚本文件
├── Roboto-Regular.ttf     # 字体文件 (与脚本放在一起)
└── your_photos/           # 你的原始照片文件夹
    ├── photo1.jpg
    └── photo2.jpg
```

### 3. 执行命令

打开您的终端或命令行，使用 `cd` 命令进入 `project_directory` 目录，然后运行脚本。

#### 基本用法

这是最简单的命令，它将使用所有默认设置（右下角、半透明白色、字号50）来处理 `your_photos` 文件夹里的所有图片。

```bash
python watermark.py ./your_photos
```

#### 进阶用法

您可以通过添加可选参数来完全控制水印的样式。

例如，我们想把水印放在**左上角**，使用**黄色**，并且字体大小设置为 **80**：

```bash
python watermark.py ./your_photos --position top-left --color "yellow" --font_size 80
```

如果您想使用一个不在脚本目录下的特定字体文件（例如系统字体）：

```bash
# Windows 示例
python watermark.py ./your_photos --font "C:\Windows\Fonts\arial.ttf"

# macOS 示例
python watermark.py ./your_photos --font "/System/Library/Fonts/Supplemental/Arial.ttf"
```

## ⚙️ 所有可用参数

| 参数 (Argument)    | 说明                                                                                              | 默认值                             |
| ------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `input_path`       | **(必需)** 指向包含照片的文件夹的路径。                                                           | (无)                               |
| `--font_size`      | 水印的字体大小。                                                                                  | `50`                               |
| `--color`          | 水印的颜色。支持颜色名 (如 `white`)、十六进制 (如 `#FF0000`) 或 RGBA 值 (如 `rgba(255,255,255,180)`)。 | `rgba(255, 255, 255, 180)`         |
| `--position`       | 水印在图片上的位置。可选值: `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`。      | `bottom-right`                     |
| `--font`           | 字体文件的路径。如果字体文件不在脚本同目录，请使用此参数指定其完整路径。                            | `Roboto-Regular.ttf`               |


## 📂 输出结果

程序运行后，会在你的原始照片文件夹内创建一个新的子目录，命名为 `[原文件夹名]_watermark`。所有处理好的图片都会保存在这里。

例如，处理 `your_photos` 文件夹后，目录结构将变为：
```
project_directory/
├── watermark.py
├── Roboto-Regular.ttf
└── your_photos/
    ├── photo1.jpg
    ├── photo2.jpg
    └── your_photos_watermark/  <-- 新建的输出目录
        ├── photo1.jpg          <-- 带水印的图片
        └── photo2.jpg
```

## 🤔 常见问题解答

**Q1: 图片上没有出现水印，或者程序提示 "找不到字体文件"？**
**A:** 这是最常见的问题，原因通常是脚本找不到字体文件。请检查：
1.  你是否已经下载了 `.ttf` 字体文件？
2.  字体文件是否与 `watermark.py` 脚本放在了**同一个文件夹**下？
3.  如果字体在别处，你是否使用了 `--font` 参数并且指定了它的**完整**、正确的路径？

**Q2: 为什么有些图片没有被处理？**
**A:** 请检查：
1.  该图片是否为支持的格式（`.jpg`, `.jpeg`, `.tiff`）？
2.  该图片是否包含有效的 EXIF 拍摄日期信息？如果图片没有这个信息，脚本会打印一条警告并跳过它。