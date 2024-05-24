import cv2
import numpy as np
import random
from typing import List
import os


def logical_and_attack(images: List[np.ndarray]) -> np.ndarray:
    result = np.bitwise_and.reduce(images)
    return result


def logical_or_attack(images: List[np.ndarray]) -> np.ndarray:
    result = np.bitwise_or.reduce(images)
    return result


def random_selection_attack(images: List[np.ndarray]) -> np.ndarray:
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            if all(bit == bits[0] for bit in bits):
                result[i, j] = bits[0]
            else:
                result[i, j] = random.choice([0, 1])
    return result


def majority_strategy_attack(images: List[np.ndarray]) -> np.ndarray:
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            if bits.count(1) > bits.count(0):
                result[i, j] = 1
            elif bits.count(0) > bits.count(1):
                result[i, j] = 0
            else:
                result[i, j] = random.choice([0, 1])
    return result


def minority_strategy_attack(images: List[np.ndarray]) -> np.ndarray:
    height, width = images[0].shape
    result = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            bits = [image[i, j] for image in images]
            if bits.count(1) < bits.count(0):
                result[i, j] = 1
            elif bits.count(0) < bits.count(1):
                result[i, j] = 0
            else:
                result[i, j] = random.choice([0, 1])
    return result


def main():
    input_dir = './data/fingerprinted_versions'
    output_dir = './data/colluded_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 创建作品ID到图像路径的映射
    work_to_images = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg"):
            work_id = filename.split('_')[0]
            if work_id not in work_to_images:
                work_to_images[work_id] = []
            work_to_images[work_id].append(os.path.join(input_dir, filename))

    # 对每个作品ID执行共谋攻击
    for work_id, image_paths in work_to_images.items():
        images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in image_paths]
        if not all(image.shape == images[0].shape for image in images):
            raise ValueError("所有图像必须具有相同的尺寸")

        # 执行逻辑与攻击
        and_result = logical_and_attack(images)
        cv2.imwrite(os.path.join(output_dir, f"{work_id}_and_attack_result.jpg"), and_result)

        # 执行逻辑或攻击
        or_result = logical_or_attack(images)
        cv2.imwrite(os.path.join(output_dir, f"{work_id}_or_attack_result.jpg"), or_result)

        # 执行随机选取攻击
        random_result = random_selection_attack(images)
        cv2.imwrite(os.path.join(output_dir, f"{work_id}_random_attack_result.jpg"), random_result)

        # 执行最大策略攻击
        majority_result = majority_strategy_attack(images)
        cv2.imwrite(os.path.join(output_dir, f"{work_id}_majority_attack_result.jpg"), majority_result)

        # 执行最小策略攻击
        minority_result = minority_strategy_attack(images)
        cv2.imwrite(os.path.join(output_dir, f"{work_id}_minority_attack_result.jpg"), minority_result)

if __name__ == "__main__":
    main()