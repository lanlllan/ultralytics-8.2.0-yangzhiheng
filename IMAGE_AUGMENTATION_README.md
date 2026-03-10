# 图片数据增强工具使用说明

## 功能简介

这个工具可以批量处理图片训练集，自动生成多个变体以增强数据集的多样性。支持以下调整：

1. **亮度调整**：-50（变暗）→ xxx-1.jpg，+50（变亮）→ xxx-2.jpg
2. **饱和度调整**：+100（高饱和）→ xxx-3.jpg，-100（低饱和/黑白）→ xxx-4.jpg
3. **色温调整**：+100（暖色调）→ xxx-5.jpg，-100（冷色调）→ xxx-6.jpg

## 环境要求

```bash
pip install pillow numpy
```

## 使用方法

### 方式1：交互式运行（推荐）

直接运行脚本，按照提示操作：

```bash
python batch_image_augmentation.py
```

会提示选择：
- 选项1：批量处理默认目录 `./datasets/bvn/images/val`
- 选项2：处理单个文件
- 选项3：自定义目录

### 方式2：批量处理指定目录

```bash
python batch_image_augmentation.py <目录路径> [匹配模式] [输出目录]
```

**示例：**

```bash
# 处理 datasets/bvn/images/val 目录下所有 *-0.jpg 文件
python batch_image_augmentation.py ./datasets/bvn/images/val "*-0.jpg"

# 处理所有 .jpg 文件
python batch_image_augmentation.py ./datasets/bvn/images/val "*.jpg"

# 指定输出目录
python batch_image_augmentation.py ./datasets/bvn/images/val "*-0.jpg" ./output
```

### 方式3：处理单个文件

```bash
python batch_image_augmentation.py <图片路径> [输出目录]
```

**示例：**

```bash
# 在原目录生成变体
python batch_image_augmentation.py ./datasets/bvn/images/val/001-0-0.jpg

# 指定输出目录
python batch_image_augmentation.py ./datasets/bvn/images/val/001-0-0.jpg ./output
```

## 输入输出示例

**输入：** `001-0-0.jpg`（原始图片）

**输出：**
- `001-0-1.jpg` - 亮度 -50（变暗）
- `001-0-2.jpg` - 亮度 +50（变亮）
- `001-0-3.jpg` - 饱和度 +100（高饱和）
- `001-0-4.jpg` - 饱和度 -100（低饱和/黑白）
- `001-0-5.jpg` - 色温 +100（暖色调，偏红）
- `001-0-6.jpg` - 色温 -100（冷色调，偏蓝）

## 命名规则说明

脚本会自动识别文件名格式：
- 如果输入是 `xxx-0.jpg` 或 `xxx-0-0.jpg`，会自动提取基础名称 `xxx`
- 生成的文件命名为：`xxx-1.jpg`, `xxx-2.jpg`, ..., `xxx-6.jpg`

## 参数说明

### 亮度调整（Brightness）
- 参数范围：-100 到 +100
- -100：完全变暗（接近黑色）
- 0：保持原始亮度
- +100：亮度翻倍

### 饱和度调整（Saturation）
- 参数范围：-100 到 +100
- -100：完全去饱和（灰度图/黑白）
- 0：保持原始饱和度
- +100：饱和度翻倍（颜色更鲜艳）

### 色温调整（Color Temperature）
- 参数范围：-100 到 +100
- -100：冷色调（增加蓝色，减少红色）
- 0：保持原始色温
- +100：暖色调（增加红色，减少蓝色）

## 高级用法

### 在 Python 代码中调用

```python
from batch_image_augmentation import process_single_image, batch_process_directory

# 处理单个文件
process_single_image("./datasets/bvn/images/val/001-0-0.jpg")

# 批量处理目录
batch_process_directory(
    input_dir="./datasets/bvn/images/val",
    pattern="*-0.jpg",
    output_dir=None  # None表示输出到原目录
)
```

### 自定义调整参数

如果需要修改调整参数（如改变亮度、饱和度、色温的具体数值），可以编辑 `batch_image_augmentation.py` 文件中的相关代码。

## 注意事项

1. **图片格式**：支持 JPG、JPEG、PNG 等常见格式
2. **质量设置**：默认保存质量为 95，可在代码中修改
3. **文件覆盖**：如果输出文件已存在，会被覆盖
4. **颜色模式**：自动转换为 RGB 模式处理
5. **内存使用**：大图片或大批量处理时注意内存占用

## 常见问题

**Q: 为什么生成的图片文件大小不一样？**
A: 不同的亮度、饱和度会影响 JPEG 压缩效果，导致文件大小不同。

**Q: 可以同时处理多个目录吗？**
A: 目前不支持，但可以多次运行脚本处理不同目录。

**Q: 如何批量处理训练集和验证集？**
A: 分别运行两次脚本，指定不同的目录即可。

```bash
# 处理训练集
python batch_image_augmentation.py ./datasets/bvn/images/train "*-0.jpg"

# 处理验证集
python batch_image_augmentation.py ./datasets/bvn/images/val "*-0.jpg"
```

## 技术细节

- **亮度调整**：使用 `PIL.ImageEnhance.Brightness`
- **饱和度调整**：使用 `PIL.ImageEnhance.Color`
- **色温调整**：通过 numpy 数组操作 RGB 通道实现

## 许可与贡献

欢迎提出改进建议和问题反馈！
