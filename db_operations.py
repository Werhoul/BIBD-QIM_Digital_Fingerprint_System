import os
import cv2
import configparser
import mysql.connector
from datetime import datetime
import numpy as np
from qim import QIM, extract_fingerprint, calculate_image_capacity

# 导入QIM类和相关图像处理函数
from qim import embed_fingerprint, check_fingerprint_length

# 导入生成数字指纹的函数
from fingerprint import generate_digital_fingerprint


class DatabaseManager:
    def __init__(self, host, user, password, database):
        # 尝试连接到指定的数据库
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database  # 确保这里的数据库名称与您创建的数据库名称匹配
            )
            self.cursor = self.db_connection.cursor()
            print("Database connection successful")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")


    def insert_fingerprint_record(self, user_id, work_id, fingerprint, distribution_time):
        try:
            sql = """
            INSERT INTO digital_fingerprints (user_id, work_id, digital_fingerprint, distribution_time)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (user_id, work_id, fingerprint, distribution_time))
            self.db_connection.commit()
            print("Record inserted successfully")
        except mysql.connector.Error as err:
            print(f"Failed to insert record: {err}")

    def get_work_name(self, work_id):
        try:
            sql = "SELECT work_name FROM works WHERE work_id = %s"
            self.cursor.execute(sql, (work_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"No work found with work_id {work_id}")
        except mysql.connector.Error as err:
            print(f"Database query error: {err}")
            return None

    def get_all_user_ids(self):
        try:
            sql = "SELECT user_id FROM users"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return [item[0] for item in results]
        except mysql.connector.Error as err:
            print(f"Database query error: {err}")
            return []

    def fetch_all_fingerprints(self):
        sql = "SELECT user_id, work_id, digital_fingerprint FROM digital_fingerprints"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()
            print("MySQL connection is closed")


def process_image_for_distribution(db_manager,user_id, work_id, qim_delta, original_images_folder, fingerprinted_versions_folder):
    # 确保你在主函数中初始化了 QIM 实例
    qim = QIM(delta = qim_delta)

    try:
        # 从数据库获取work_name
        work_name = db_manager.get_work_name(work_id)
        if work_name is None:
            raise ValueError("Work name not found for the provided work ID.")

        # 构建图像路径
        image_path = os.path.join(original_images_folder, f'{work_name}.jpg')
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError(f"No image found at {image_path}")

        # 生成数字指纹
        fingerprint = generate_digital_fingerprint(user_id, work_id)

        # 检查图像容量是否足够
        if check_fingerprint_length(image, fingerprint):
            # 嵌入数字指纹
            embedded_image = embed_fingerprint(image, fingerprint, qim)

            # 保存处理后的图像
            embedded_image_path = os.path.join(fingerprinted_versions_folder, f'{work_id}_{user_id}.jpg')
            cv2.imwrite(embedded_image_path, embedded_image)
            print(f"指纹嵌入完成，保存嵌入后的图像为 {embedded_image_path}")

            # 记录到数据库
            db_manager.insert_fingerprint_record(user_id, work_id, fingerprint, datetime.now())
            db_manager.close()

            return True

    except Exception as e:
        print(f"Error processing image for user {user_id} and work {work_id}: {e}")
        db_manager.close()
        return False


def trace_colluder(db_manager, colluded_images_path, qim_delta):
    # 提取文件名中的work_id
    filename = os.path.basename(colluded_images_path)
    parts = filename.split('_')
    if len(parts) < 2:  # 确保文件名至少包含一个下划线
        raise ValueError("Invalid filename format. Expected 'work_id_attackmethod.ext'.")
    work_id = parts[0]

    # 读取合谋攻击生成的图像
    image = cv2.imread(colluded_images_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"No image found at {colluded_images_path}")

    # 提取数字指纹
    qim = QIM(delta=qim_delta)
    fingerprint_length = calculate_image_capacity(image)
    extracted_fingerprint = extract_fingerprint(image, qim, fingerprint_length)

    # 获取数据库中所有的数字指纹记录
    all_fingerprints = db_manager.fetch_all_fingerprints()

    # 比对提取的指纹和数据库中的指纹
    for record in all_fingerprints:
        user_id, stored_work_id, stored_fingerprint = record
        if work_id == stored_work_id:
            stored_fingerprint = np.frombuffer(stored_fingerprint, dtype=np.uint8)
            if np.array_equal(extracted_fingerprint, stored_fingerprint):
                print(f"Match found: User ID = {user_id}, Work ID = {stored_work_id}")
                print("Collusion detection completed successfully.")
                return True

    print("No match found. Unable to trace the colluder. Failed to detect collusion.")
    return False
