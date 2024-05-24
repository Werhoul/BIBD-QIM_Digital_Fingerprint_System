from bibdcalc import BIBD
import hashlib
import numpy as np

def generate_digital_fingerprint(user_id, work_id):
    """
    根据用户信息和作品标识生成对应的数字指纹编码。
    参数:
    user_id (str): 用户唯一标识符 (9位数字)。
    work_id (str): 作品唯一标识符。
    返回:
    str: 生成的数字指纹编码。
    """
    # 结合用户ID和作品ID生成哈希值作为种子
    combined_id = f"{user_id}-{work_id}"
    seed = int(hashlib.sha256(combined_id.encode()).hexdigest(), 16) % 10**8

    # 根据种子生成有限域的加法和乘法表
    add_table, mult_table = generate_finite_field_tables(seed)

    # 使用 BIBD 生成数字指纹编码
    bibd = BIBD.create_projective_plane(add_table, mult_table)
    # print("BIBD Blocks:", bibd)  # 输出 BIBD 结构的块

    # 获取 BIBD 参数
    incidency_matrix = bibd.get_incidency_matrix()
    # print("Incidency Matrix:", incidency_matrix)  # 输出事件矩阵

    # 将 BIBD 的事件矩阵转化为字符串作为数字指纹编码
    fingerprint = ''.join(incidency_matrix)
    # print("Generated Fingerprint:", fingerprint)  # 输出数字指纹编码

    # 输出数字指纹的长度
    print(f"生成的数字指纹长度为: {len(fingerprint)} 位")

    return fingerprint

def generate_finite_field_tables(seed):
    """
    根据种子生成有限域的加法表和乘法表。
    参数:
    seed (int): 用于生成表的种子。
    返回:
    tuple: 加法表和乘法表。
    """
    np.random.seed(seed)  # 设置随机种子确保结果的可重现性

    field_size = 7  # 示例有限域大小
    # 创建标准加法和乘法表
    standard_add = np.array([(i + j) % field_size for i in range(field_size) for j in range(field_size)]).reshape(field_size, field_size)
    standard_mult = np.array([(i * j) % field_size for i in range(field_size) for j in range(field_size)]).reshape(field_size, field_size)

    # 随机置换这些表来生成不同的有限域表
    permutation = np.random.permutation(field_size)
    add_table = standard_add[permutation, :][:, permutation]
    mult_table = standard_mult[permutation, :][:, permutation]

    return add_table.tolist(), mult_table.tolist()


if __name__ == "__main__":
    # 不同用户同一作品的测试
    work_id = '5156354548'  # 示例作品ID
    user_ids = ['123456789', '987654321', '555666777']  # 示例用户ID列表
    fingerprints = []

    for user_id in user_ids:
        fingerprint = generate_digital_fingerprint(user_id, work_id)
        fingerprints.append((user_id, fingerprint))
        print(f"用户 {user_id} 的作品 {work_id} 的数字指纹编码为: {fingerprint}")
