import struct

# 定义MD5算法需要用到的常量
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476


# 定义辅助函数
def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def pad_message(message):
    original_length = len(message) * 8
    message += b"\x80"
    padding = (56 - (len(message) % 64)) % 64
    message += b"\x00" * padding
    message += struct.pack("<Q", original_length)
    return message


# 定义MD5算法主函数
def md5(message):
    # 初始化变量
    a = A
    b = B
    c = C
    d = D

    # 分组处理
    for i in range(0, len(message), 64):
        chunk = message[i : i + 64]

        # 将每个分组划分为16个32位的字
        words = struct.unpack("<16I", chunk)

        # 初始化哈希值
        aa = a
        bb = b
        cc = c
        dd = d

        # 主循环
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            temp = d
            d = c
            c = b
            b = (b + left_rotate((a + f + 0x5A827999 + words[g]), 7)) & 0xFFFFFFFF
            a = temp

        # 更新哈希值
        a = (a + aa) & 0xFFFFFFFF
        b = (b + bb) & 0xFFFFFFFF
        c = (c + cc) & 0xFFFFFFFF
        d = (d + dd) & 0xFFFFFFFF

    # 返回最终的哈希值
    return struct.pack("<4I", a, b, c, d)


# 计算文件的MD5摘要
def calculate_md5(filename):
    with open(filename, "rb") as file:
        md5_hash = md5(pad_message(file.read()))
    return md5_hash.hex()


# filename = "test1.doc"
# md5_hash = calculate_md5(filename)
# print("MD5 hash:", md5_hash)


# 在上述代码中，我们首先定义了MD5算法中使用的常量A、B、C、D，这些常量将作为初始的哈希值。
# 接下来，我们定义了一些辅助函数。left_rotate函数用于循环位移操作，将给定的32位整数x循环左移n位。
# pad_message函数用于对消息进行填充，使其长度满足MD5算法的要求。在消息末尾添加一个"1"比特，
# 然后根据需要添加"0"比特直到消息长度满足对64取余为56的条件。最后，将原始消息的长度以64位的小端序形式添加到消息末尾。
# 然后，我们定义了主函数md5，该函数接受消息作为输入，并按照MD5算法的步骤进行处理。首先，初始化变量a、b、c、d为初始哈希值。
# 然后，将消息分组处理，每个分组包含64个字节。将每个分组划分为16个32位的字，然后进行主循环，共进行64轮迭代。在每轮迭代中，
# 根据当前的轮数选择不同的逻辑函数和位移量，更新哈希值a、b、c、d。最后，将最终的哈希值返回。
# 最后，我们定义了calculate_md5函数，该函数接受文件名作为输入，并使用pad_message函数对文件内容进行填充，
# 然后调用md5函数计算文件的MD5摘要。最终，将MD5摘要以十六进制形式返回。
