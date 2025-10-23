import qrcode

def generate_qr_numeric_matrix(data_url):
    """
    为给定的 URL 生成一个二维码的数字矩阵 (1=黑, 0=白)。

    参数:
    data_url (str): 你想要编码的网址，例如 "https://www.google.com"

    返回:
    list[list[int]]: 一个二维列表 (矩阵)，其中 1 代表暗模块，0 代表亮模块。
    """
    
    # 1. 创建一个 QRCode 实例
    # 我们可以指定一些参数：
    # version: 控制二维码的大小 (1-40)。None 表示自动。
    # error_correction: 纠错级别 (L, M, Q, H)。
    # border: 边框的空白模块数 (默认是 4)。
    qr = qrcode.QRCode(
        version=None,  # 自动决定版本 (大小)
        error_correction=qrcode.constants.ERROR_CORRECT_M, # M 级别纠错
        border=4  # 默认的 4 模块边框
    )
    
    # 2. 添加数据
    qr.add_data(data_url)
    
    # 3. 生成 QR 码。fit=True 确保数据能装入自动选择的版本中。
    qr.make(fit=True)
    
    # 4. 获取矩阵 (核心)
    # qr.get_matrix() 返回一个布尔值 (Boolean) 的二维列表。
    # True 代表黑色 (暗) 模块，False 代表白色 (亮) 模块。
    bool_matrix = qr.get_matrix()
    
    # 5. 将布尔矩阵转换为数字矩阵 (1 和 0)
    # 我们使用列表推导式 (list comprehension) 来高效转换：
    # int(True) 结果为 1
    # int(False) 结果为 0
    numeric_matrix = [[int(cell) for cell in row] for row in bool_matrix]
    
    return numeric_matrix

def print_matrix_visual(matrix):
    """
    一个辅助函数，用于在终端中“画”出这个矩阵，使其看起来像二维码。
    """
    print("\n--- 矩阵可视化 (█=1,  =0) ---")
    
    # Windows 终端可能需要 '██'，而其他终端 '█' 就足够了
    # 为了兼容性，我们使用两个字符
    CHAR_BLACK = "██"
    CHAR_WHITE = "  "
    
    for row in matrix:
        line = ""
        for cell in row:
            if cell == 1:
                line += CHAR_BLACK
            else:
                line += CHAR_WHITE
        print(line)

# --- 执行 ---

# 你要编码的网址
my_url = "https://rm.micdz.cn"

# 生成数字矩阵
matrix = generate_qr_numeric_matrix(my_url)

# 打印矩阵信息
print(f"--- 为 '{my_url}' 生成的数字矩阵 ---")
print(f"矩阵维度: {len(matrix)} x {len(matrix[0])}")

# 打印矩阵的前 5 行（作为数据示例）
print("\n--- 矩阵数据 (前 5 行) ---")
for i in range(min(5, len(matrix))):
    print(matrix[i])

# 可视化打印整个矩阵
print_matrix_visual(matrix)
print(matrix)