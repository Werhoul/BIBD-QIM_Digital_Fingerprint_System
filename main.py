import argparse
import configparser
import cv2
import os
from db_operations import DatabaseManager, process_image_for_distribution, trace_colluder
from colluded_attack import (
    attack_per_channel,
    logical_and_attack,
    logical_or_attack,
    random_selection_attack,
    majority_strategy_attack,
    minority_strategy_attack
)


def main():
    parser = argparse.ArgumentParser(description="Process images for distribution, perform a collusion attack, or trace a colluder.")
    parser.add_argument('--option', type=str, choices=['distri', 'cldatk', 'trace'], help='Choose "distri" for distribution, "cldatk" for collusion attack, or "trace" for tracing colluders.')
    parser.add_argument('parameters', nargs='+', help='User ID and Work ID for distribution, filenames and attack type for collusion attack, or a single filename for tracing.')
    args = parser.parse_args()

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 获取QIM delta值
    qim_delta = float(config['settings']['qim_delta'])

    # 获取文件夹路径
    original_images_folder = config['folders']['original_images_folder']
    fingerprinted_versions_folder = config['folders']['fingerprinted_versions_folder']
    colluded_images_folder = config['folders']['colluded_images_folder']

    # 获取数据库配置
    db_host = config['database']['host']
    db_user = config['database']['user']
    db_password = config['database']['password']
    db_database = config['database']['database']

    # 创建 DatabaseManager 实例
    db_manager = DatabaseManager(db_host, db_user, db_password, db_database)

    if args.option == 'distri':
        if len(args.parameters) != 2:
            print("Invalid number of arguments for image distribution.")
            return
        user_id, work_id = args.parameters
        result = process_image_for_distribution(db_manager, user_id, work_id, qim_delta, original_images_folder, fingerprinted_versions_folder)
        if result:
            print("Image processed and distributed successfully.")
        else:
            print("Failed to process and distribute image.")

    elif args.option == 'cldatk':

        if len(args.parameters) < 3:
            print("Invalid number of arguments for collusion attack.")

            return

        attack_type = args.parameters[-1]

        image_paths = args.parameters[:-1]

        images = [cv2.imread(image_path) for image_path in image_paths]

        # 检查是否所有读入的图像都是有效的，否则提醒用户

        if any(image is None for image in images):
            print("某些图像路径无效或图像文件不能读取。")

            return

        if not all(image.shape == images[0].shape for image in images):
            print("所有图像必须具有相同的尺寸以进行合谋攻击。")

            return

        attack_result = None

        if attack_type in ["and", "or", "random", "majority", "minority"]:

            if not os.path.exists(colluded_images_folder):
                os.makedirs(colluded_images_folder)

            work_id = os.path.basename(image_paths[0]).split('_')[0]

            if attack_type == "and":

                attack_result = attack_per_channel(images, logical_and_attack)

            elif attack_type == "or":

                attack_result = attack_per_channel(images, logical_or_attack)

            elif attack_type == "random":

                attack_result = attack_per_channel(images, random_selection_attack)

            elif attack_type == "majority":

                attack_result = attack_per_channel(images, majority_strategy_attack)

            elif attack_type == "minority":

                attack_result = attack_per_channel(images, minority_strategy_attack)

            if attack_result is not None:

                result_filename = os.path.join(colluded_images_folder, f"{work_id}_{attack_type}_attack_result.jpg")

                cv2.imwrite(result_filename, attack_result)

                print(f"{attack_type.capitalize()} attack executed and result saved as {result_filename}")

            else:

                print("Failed to execute the attack.")

        else:

            print("Invalid attack type specified.")

    elif args.option == 'trace':
        if len(args.parameters) != 1:
            print("Invalid number of arguments for tracing.")
            return
        colluded_image_path = args.parameters[0]
        result = trace_colluder(db_manager, colluded_image_path, qim_delta)
        if result:
            print("Colluder traced successfully.")
        else:
            print("Failed to trace the colluder.")


if __name__ == "__main__":
    main()
