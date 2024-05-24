import configparser
import sys


# 导入process_image_for_distribution函数
from db_operations import process_image_for_distribution


def main():
    # 读取配置文件来获取QIM delta值
    config = configparser.ConfigParser()
    config.read('config.ini')
    qim_delta = float(config['settings']['qim_delta'])

    # 从命令行参数获取user_id和work_id
    if len(sys.argv) != 3:
        print("Usage: python main.py <user_id> <work_id>")
        return

    user_id = sys.argv[1]
    work_id = sys.argv[2]

    # 调用图像处理函数
    result = process_image_for_distribution(user_id, work_id, qim_delta)
    if result:
        print("Image processed and distributed successfully.")
    else:
        print("Failed to process and distribute image.")

if __name__ == "__main__":
    main()
