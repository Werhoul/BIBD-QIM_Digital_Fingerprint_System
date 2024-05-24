import configparser
import sys
import random
from db_operations import process_image_for_distribution, DatabaseManager

def main():
    # 读取配置文件来获取QIM delta值
    config = configparser.ConfigParser()
    config.read('config.ini')
    qim_delta = float(config['settings']['qim_delta'])

    if len(sys.argv) < 2:
        print("Usage: python main.py --single <user_id> <work_id> OR python main.py --batch <num_users> <work_id>")
        return

    mode = sys.argv[1]
    if mode == "--single" and len(sys.argv) == 4:
        user_id = sys.argv[2]
        work_id = sys.argv[3]

        # 调用图像处理函数
        result = process_image_for_distribution(user_id, work_id, qim_delta)
        if result:
            print("Image processed and distributed successfully.")
        else:
            print("Failed to process and distribute image.")

    elif mode == "--batch" and len(sys.argv) == 4:
        num_users = int(sys.argv[2])
        if num_users < 2:
            print("Please specify at least 2 users for batch processing.")
            return
        work_id = sys.argv[3]

        # 获取用户列表并随机选择
        db_manager = DatabaseManager('localhost', 'root', 'lamcaptain11', 'DigitalFingerprintDB')
        user_ids = db_manager.get_all_user_ids()
        if len(user_ids) < num_users:
            print("Not enough users available.")
            return

        selected_users = random.sample(user_ids, num_users)
        success_count = 0
        for user_id in selected_users:
            if process_image_for_distribution(user_id, work_id, qim_delta):
                success_count += 1
                print(f"Successfully distributed to user {user_id}")

        print(f"Total successful distributions: {success_count} out of {num_users}")
        db_manager.close()
    else:
        print("Usage: python main.py --single <user_id> <work_id> OR python main.py --batch <num_users> <work_id>")

if __name__ == "__main__":
    main()
