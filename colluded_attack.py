import cv2
import numpy as np
import random
from typing import List


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


# 示例使用
def main():
    # 读取多张图像
    image_paths = ["image1.png", "image2.png", "image3.png"]
    images = [cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) for image_path in image_paths]

    # 检查所有图像是否大小一致
    if not all(image.shape == images[0].shape for image in images):
        raise ValueError("所有图像必须具有相同的尺寸")

    # 执行逻辑与攻击
    and_result = logical_and_attack(images)
    cv2.imwrite("and_attack_result.png", and_result)

    # 执行逻辑或攻击
    or_result = logical_or_attack(images)
    cv2.imwrite("or_attack_result.png", or_result)

    # 执行随机选取攻击
    random_result = random_selection_attack(images)
    cv2.imwrite("random_attack_result.png", random_result)

    # 执行最大策略攻击
    majority_result = majority_strategy_attack(images)
    cv2.imwrite("majority_attack_result.png", majority_result)

    # 执行最小策略攻击
    minority_result = minority_strategy_attack(images)
    cv2.imwrite("minority_attack_result.png", minority_result)


if __name__ == "__main__":
    main()
