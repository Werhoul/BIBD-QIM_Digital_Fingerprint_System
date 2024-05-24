import os
import cv2
import numpy as np
from typing import List
import random
from functools import wraps

def with_attack_name(func):
    @wraps(func)
    def wrapper(images, channel=None):
        attack_name = func.__name__
        if channel is None:
            print(f"开始执行 {attack_name} 攻击")
        else:
            print(f"开始处理通道 {channel}")
        result = func(images)
        if channel is not None:
            print(f"处理通道 {channel} 处理完成")
        return result
    return wrapper

def attack_per_channel(images: List[np.ndarray], attack_func):
    """
    对每个颜色通道分别应用指定的攻击函数。
    :param images: 包含多个彩色图像的列表。
    :param attack_func: 要应用的攻击函数。
    :return: 应用攻击后的图像。
    """
    height, width, channels = images[0].shape
    result = np.zeros((height, width, channels), dtype=np.uint8)
    print(f"开始执行 {attack_func.__name__} 攻击")
    for channel in range(channels):
        channel_images = [img[:, :, channel] for img in images]
        result[:, :, channel] = attack_func(channel_images, channel)
    print(f"{attack_func.__name__} 攻击完成")
    return result

@with_attack_name
def logical_and_attack(images: List[np.ndarray], channel=None) -> np.ndarray:
    """
    对图像列表执行逻辑与攻击。
    :param images: 彩色或灰度图像的列表。
    :return: 攻击后的图像。
    """
    return np.bitwise_and.reduce(images)

@with_attack_name
def logical_or_attack(images: List[np.ndarray], channel=None) -> np.ndarray:
    """
    对图像列表执行逻辑或攻击。
    :param images: 彩色或灰度图像的列表。
    :return: 攻击后的图像。
    """
    return np.bitwise_or.reduce(images)

@with_attack_name
def random_selection_attack(images: List[np.ndarray], channel=None) -> np.ndarray:
    """
    对图像列表执行随机选择攻击。
    :param images: 单通道图像列表。
    :return: 攻击后的图像。
    """
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            result[i, j] = random.choice(bits)
    return result

@with_attack_name
def majority_strategy_attack(images: List[np.ndarray], channel=None) -> np.ndarray:
    """
    对图像列表执行多数策略攻击。
    :param images: 单通道图像列表。
    :return: 攻击后的图像。
    """
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=images[0].dtype)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            result[i, j] = 255 if bits.count(255) > bits.count(0) else 0
    return result

@with_attack_name
def minority_strategy_attack(images: List[np.ndarray], channel=None) -> np.ndarray:
    """
    对图像列表执行少数策略攻击。
    :param images: 单通道图像列表。
    :return: 攻击后的图像。
    """
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=images[0].dtype)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            result[i, j] = 255 if bits.count(255) <= bits.count(0) else 0
    return result

def load_images_by_work_id(input_dir: str, work_id: str) -> List[np.ndarray]:
    """
    读取包含特定作品ID的所有图像，并将其加载到一个图像列表中。
    :param input_dir: 图像文件的输入目录。
    :param work_id: 作品ID。
    :return: 加载的图像列表。
    """
    images = []
    for filename in os.listdir(input_dir):
        if filename.startswith(work_id) and filename.endswith(".jpg"):
            image_path = os.path.join(input_dir, filename)
            images.append(cv2.imread(image_path))
    if not images:
        raise ValueError(f"在目录 {input_dir} 中未找到作品ID为 {work_id} 的图像")
    return images

def main():
    """
    主函数，执行合谋攻击并保存结果图像。
    """
    input_dir = './data/fingerprinted_versions'
    output_dir = './data/colluded_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    work_id = "2CBD8C1F2"
    images = load_images_by_work_id(input_dir, work_id)

    # 对每种攻击，逐通道处理
    and_result = attack_per_channel(images, logical_and_attack)
    print(f"{work_id} 的 logical_and_attack 攻击结果已保存。")
    cv2.imwrite(os.path.join(output_dir, f"{work_id}_and_attack_result.jpg"), and_result)

    or_result = attack_per_channel(images, logical_or_attack)
    print(f"{work_id} 的 logical_or_attack 攻击结果已保存。")
    cv2.imwrite(os.path.join(output_dir, f"{work_id}_or_attack_result.jpg"), or_result)

    random_result = attack_per_channel(images, random_selection_attack)
    print(f"{work_id} 的 random_selection_attack 攻击结果已保存。")
    cv2.imwrite(os.path.join(output_dir, f"{work_id}_random_attack_result.jpg"), random_result)

    majority_result = attack_per_channel(images, majority_strategy_attack)
    print(f"{work_id} 的 majority_strategy_attack 攻击结果已保存。")
    cv2.imwrite(os.path.join(output_dir, f"{work_id}_majority_attack_result.jpg"), majority_result)

    minority_result = attack_per_channel(images, minority_strategy_attack)
    print(f"{work_id} 的 minority_strategy_attack 攻击结果已保存。")
    cv2.imwrite(os.path.join(output_dir, f"{work_id}_minority_attack_result.jpg"), minority_result)

if __name__ == "__main__":
    main()
