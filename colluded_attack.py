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
