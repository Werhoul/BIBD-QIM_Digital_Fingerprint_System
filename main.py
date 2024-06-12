import argparse
import configparser
import cv2
from colluded_attack import (
    logical_and_attack,
    logical_or_attack,
    random_selection_attack,
    majority_strategy_attack,
    minority_strategy_attack
)

# 导入process_image_for_distribution函数
from db_operations import process_image_for_distribution


def main():
    parser = argparse.ArgumentParser(description="Process images for distribution or perform a collusion attack.")
    parser.add_argument('--option', type=str, choices=['distri', 'cldatk'], help='Choose "distri" for distribution or "cldatk" for collusion attack')
    parser.add_argument('parameters', nargs='+', help='User ID and Work ID for distribution or filenames and attack type for collusion attack')
    args = parser.parse_args()

    # 首先读取配置文件来获取QIM delta值
    config = configparser.ConfigParser()
    config.read('config.ini')
    qim_delta = float(config['settings']['qim_delta'])

    if args.option == 'distri':
        if len(args.parameters) != 2:
            print("Invalid number of arguments for image distribution.")
            return
        user_id = args.parameters[0]
        work_id = args.parameters[1]
        result = process_image_for_distribution(user_id, work_id, qim_delta)
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
        images = [cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) for image_path in image_paths]

        if not all(image.shape == images[0].shape for image in images):
            raise ValueError("所有图像必须具有相同的尺寸")

        attack_result = None
        if attack_type in ["and", "or", "random", "majority", "minority"]:
            if attack_type == "and":
                attack_result = logical_and_attack(images)
            elif attack_type == "or":
                attack_result = logical_or_attack(images)
            elif attack_type == "random":
                attack_result = random_selection_attack(images)
            elif attack_type == "majority":
                attack_result = majority_strategy_attack(images)
            elif attack_type == "minority":
                attack_result = minority_strategy_attack(images)

            if attack_result is not None:
                result_filename = f"{attack_type}_attack_result.png"
                cv2.imwrite(result_filename, attack_result)
                print(f"{attack_type.capitalize()} attack executed and result saved as {result_filename}")
            else:
                print("Failed to execute the attack.")
        else:
            print("Invalid attack type specified.")


if __name__ == "__main__":
    main()
