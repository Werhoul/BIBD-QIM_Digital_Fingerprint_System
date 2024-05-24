import cv2
import numpy as np
import os


class QIM:
    def __init__(self, delta):
        self.delta = delta

    def embed(self, x, m):
        x = x.astype(float)
        d = self.delta
        y = np.round(x / d) * d + (-1) ** (m + 1) * d / 4
        return y

    def detect(self, z):
        shape = z.shape
        z = z.flatten()
        m_detected = np.zeros_like(z, dtype=float)
        z_detected = np.zeros_like(z, dtype=float)
        z0 = self.embed(z, 0)
        z1 = self.embed(z, 1)
        d0 = np.abs(z - z0)
        d1 = np.abs(z - z1)

        for i, (dd0, dd1) in enumerate(zip(d0, d1)):
            if dd0 < dd1:
                m_detected[i] = 0
                z_detected[i] = z0[i]
            else:
                m_detected[i] = 1
                z_detected[i] = z1[i]

        z_detected = z_detected.reshape(shape)
        m_detected = m_detected.reshape(shape)
        return z_detected, m_detected.astype(int)


def calculate_image_capacity(image):
    height, width = image.shape[:2]
    return height * width


def check_fingerprint_length(image, fingerprint):
    capacity = calculate_image_capacity(image)
    if len(fingerprint) > capacity:
        raise ValueError("指纹长度超过图像可嵌入容量，无法嵌入")
    else:
        print("图像可嵌入容量足够，继续进行嵌入操作")
        return True


def pad_fingerprint(fingerprint, target_length):
    padded_fingerprint = fingerprint + '0' * (target_length - len(fingerprint))
    return padded_fingerprint


def embed_fingerprint(image, fingerprint, qim):
    flat_image = image.flatten()
    capacity = len(flat_image)
    padded_fingerprint = pad_fingerprint(fingerprint, capacity)
    fingerprint_array = np.array([int(bit) for bit in padded_fingerprint])
    embedded_image = qim.embed(flat_image, fingerprint_array)
    embedded_image = embedded_image.reshape(image.shape)
    return embedded_image


def extract_fingerprint(embedded_image, qim, fingerprint_length):
    _, extracted_fingerprint = qim.detect(embedded_image)
    extracted_fingerprint_str = ''.join(map(str, extracted_fingerprint.flatten()[:fingerprint_length]))
    return extracted_fingerprint_str


if __name__ == "__main__":
    # 直接赋值读入文件和输出文件夹的路径
    original_images_folder = 'path/to/original/images'
    fingerprinted_versions_folder = 'path/to/fingerprinted/versions'

    # 读入指定图像
    image_path = os.path.join(original_images_folder, "color_image.jpg")
    # 随机生成长度为1024的二进制数字指纹
    fingerprint = ''.join(np.random.choice(['0', '1'], size=1024))

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("无法读取图像，请检查图像路径")

    qim = QIM(delta=0.1)

    try:
        if check_fingerprint_length(image, fingerprint):
            embedded_image = embed_fingerprint(image, fingerprint, qim)
            embedded_image_path = os.path.join(fingerprinted_versions_folder, "embedded_image.jpg")
            cv2.imwrite(embedded_image_path, embedded_image)
            print(f"指纹嵌入完成，保存嵌入后的图像为 {embedded_image_path}")

            extracted_fingerprint = extract_fingerprint(embedded_image, qim, len(fingerprint))
            print("提取的指纹:", extracted_fingerprint)

            if extracted_fingerprint == fingerprint:
                print("提取的指纹与嵌入的指纹一致")
            else:
                print("提取的指纹与嵌入的指纹不一致")
    except ValueError as e:
        print(e)
