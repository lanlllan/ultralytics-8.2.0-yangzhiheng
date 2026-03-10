"""
批量图片数据增强脚本
功能：对原始图片进行亮度、饱和度、色温调整，生成训练集变体
用法：python batch_image_augmentation.py
"""

import os
from PIL import Image, ImageEnhance
import numpy as np
from pathlib import Path


def adjust_brightness(image, factor):
    """
    调整图片亮度
    :param image: PIL Image对象
    :param factor: 亮度因子，-100到100的值会被转换为合适的增强因子
    :return: 调整后的图片
    """
    # 将-100到100的范围转换为0到2的增强因子
    # -100 -> 0 (完全变暗)
    # 0 -> 1 (原始亮度)
    # 100 -> 2 (亮度翻倍)
    enhancer_factor = 1 + (factor / 100)
    enhancer_factor = max(0, min(2, enhancer_factor))
    
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(enhancer_factor)


def adjust_saturation(image, factor):
    """
    调整图片饱和度
    :param image: PIL Image对象
    :param factor: 饱和度因子，-100到100
    :return: 调整后的图片
    """
    # 将-100到100的范围转换为0到2的增强因子
    enhancer_factor = 1 + (factor / 100)
    enhancer_factor = max(0, min(2, enhancer_factor))
    
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(enhancer_factor)


def adjust_color_temperature(image, factor):
    """
    调整图片色温
    :param image: PIL Image对象
    :param factor: 色温因子，-100到100
                  正值：增加暖色调（增加红色，减少蓝色）
                  负值：增加冷色调（减少红色，增加蓝色）
    :return: 调整后的图片
    """
    # 转换为RGB numpy数组
    img_array = np.array(image, dtype=np.float32)
    
    # 根据factor调整色温
    # factor范围：-100到100
    # 正值：暖色调，增强红色通道，减弱蓝色通道
    # 负值：冷色调，减弱红色通道，增强蓝色通道
    
    red_adjust = 1 + (factor / 200)  # -100: 0.5, 0: 1.0, 100: 1.5
    blue_adjust = 1 - (factor / 200)  # -100: 1.5, 0: 1.0, 100: 0.5
    
    img_array[:, :, 0] = np.clip(img_array[:, :, 0] * red_adjust, 0, 255)  # Red
    img_array[:, :, 2] = np.clip(img_array[:, :, 2] * blue_adjust, 0, 255)  # Blue
    
    return Image.fromarray(img_array.astype(np.uint8))


def process_single_image(input_path, output_dir=None):
    """
    处理单张图片，生成6个变体
    :param input_path: 输入图片路径（如：001-0-0.jpg）
    :param output_dir: 输出目录，如果为None则与输入图片同目录
    :return: 处理的文件列表
    """
    input_path = Path(input_path)
    
    # 检查文件是否存在
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        return []
    
    # 确定输出目录
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 解析文件名（假设格式为：xxx-0.jpg 或 xxx-0-0.jpg）
    stem = input_path.stem  # 不含扩展名的文件名
    ext = input_path.suffix  # 扩展名
    
    # 移除最后的-0后缀（如果有）
    if stem.endswith('-0'):
        base_name = stem[:-2]
    else:
        base_name = stem
    
    print(f"\n📷 处理图片: {input_path.name}")
    print(f"   基础名称: {base_name}")
    
    try:
        # 打开原始图片
        img = Image.open(input_path)
        
        # 确保是RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        processed_files = []
        
        # 1. 亮度 -50 (变暗)
        output_path = output_dir / f"{base_name}-1{ext}"
        print(f"   生成: {output_path.name} (亮度: -50)")
        img_adjusted = adjust_brightness(img, -50)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        # 2. 亮度 +50 (变亮)
        output_path = output_dir / f"{base_name}-2{ext}"
        print(f"   生成: {output_path.name} (亮度: +50)")
        img_adjusted = adjust_brightness(img, 50)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        # 3. 饱和度 +100 (高饱和)
        output_path = output_dir / f"{base_name}-3{ext}"
        print(f"   生成: {output_path.name} (饱和度: +100)")
        img_adjusted = adjust_saturation(img, 100)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        # 4. 饱和度 -100 (低饱和/黑白)
        output_path = output_dir / f"{base_name}-4{ext}"
        print(f"   生成: {output_path.name} (饱和度: -100)")
        img_adjusted = adjust_saturation(img, -100)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        # 5. 色温 +100 (暖色调)
        output_path = output_dir / f"{base_name}-5{ext}"
        print(f"   生成: {output_path.name} (色温: +100)")
        img_adjusted = adjust_color_temperature(img, 100)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        # 6. 色温 -100 (冷色调)
        output_path = output_dir / f"{base_name}-6{ext}"
        print(f"   生成: {output_path.name} (色温: -100)")
        img_adjusted = adjust_color_temperature(img, -100)
        img_adjusted.save(output_path, quality=95)
        processed_files.append(output_path)
        
        print(f"✅ 完成！生成了 {len(processed_files)} 个变体")
        return processed_files
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return []


def batch_process_directory(input_dir, pattern="*-0.jpg", output_dir=None):
    """
    批量处理目录中的图片
    :param input_dir: 输入目录路径
    :param pattern: 文件匹配模式，默认为 *-0.jpg
    :param output_dir: 输出目录，如果为None则与输入图片同目录
    :return: 处理的文件总数
    """
    input_dir = Path(input_dir)
    
    if not input_dir.exists():
        print(f"❌ 目录不存在: {input_dir}")
        return 0
    
    # 查找所有匹配的原始图片
    image_files = sorted(input_dir.glob(pattern))
    
    if not image_files:
        print(f"⚠️ 未找到匹配 '{pattern}' 的图片文件")
        print(f"   搜索目录: {input_dir}")
        return 0
    
    print(f"\n🔍 找到 {len(image_files)} 个待处理的图片")
    print(f"   输入目录: {input_dir}")
    if output_dir:
        print(f"   输出目录: {output_dir}")
    print("-" * 60)
    
    total_processed = 0
    for img_path in image_files:
        result = process_single_image(img_path, output_dir)
        total_processed += len(result)
    
    print("\n" + "=" * 60)
    print(f"🎉 批量处理完成！")
    print(f"   处理图片数: {len(image_files)}")
    print(f"   生成文件数: {total_processed}")
    print("=" * 60)
    
    return total_processed


if __name__ == "__main__":
    import sys
    
    # 默认处理目录
    default_input_dir = "./datasets/bvn/images/val"
    
    print("=" * 60)
    print("  图片数据增强工具")
    print("  支持亮度、饱和度、色温调整")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 单文件模式
        if sys.argv[1].endswith(('.jpg', '.jpeg', '.png')):
            input_file = sys.argv[1]
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            process_single_image(input_file, output_dir)
        # 目录批量模式
        else:
            input_dir = sys.argv[1]
            pattern = sys.argv[2] if len(sys.argv) > 2 else "*-0.jpg"
            output_dir = sys.argv[3] if len(sys.argv) > 3 else None
            batch_process_directory(input_dir, pattern, output_dir)
    else:
        # 默认批量处理模式
        print("\n请选择处理模式：")
        print("1. 批量处理目录（默认: ./datasets/bvn/images/val）")
        print("2. 处理单个文件")
        print("3. 自定义目录")
        
        choice = input("\n请输入选项 (1/2/3，直接回车选择1): ").strip() or "1"
        
        if choice == "1":
            # 批量处理默认目录
            batch_process_directory(default_input_dir, "*-0.jpg")
            
        elif choice == "2":
            # 单文件处理
            file_path = input("请输入图片文件路径: ").strip()
            if file_path:
                process_single_image(file_path)
            else:
                print("❌ 未输入文件路径")
                
        elif choice == "3":
            # 自定义目录
            dir_path = input("请输入目录路径: ").strip()
            pattern = input("请输入文件匹配模式 (默认: *-0.jpg): ").strip() or "*-0.jpg"
            if dir_path:
                batch_process_directory(dir_path, pattern)
            else:
                print("❌ 未输入目录路径")
        else:
            print("❌ 无效的选项")
