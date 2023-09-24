# 测试程序
import os
import random
import string
import multiprocessing
import file2

# 生成一个随机字符串作为密钥
# def generate_key(length=16):
# return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# def generate_file(filename, size):
# with open(filename, 'wb') as f:
# f.write(os.urandom(size))


# 测试函数
def test_file_transfer():
    filename = "test1.doc"
    # generate_file(filename, 1024 * 1024)  # 生成一个1MB的文件

    # 生成一个随机密钥
    # key = file2.generate_key()
    # dekey = key.decode("utf-8", "ignore")
    # print("random key:", dekey)

    # 运行服务器
    server_process = multiprocessing.Process(target=file2.server, args=(filename,))
    server_process.start()

    # 运行客户端
    client_process = multiprocessing.Process(target=file2.client, args=(filename,))
    client_process.start()

    # 等待客户端完成
    client_process.join()

    # 等待服务器完成
    server_process.terminate()
    server_process.join()

    # 检查传输后的文件是否和原文件一致
    with open(filename, "rb") as f:
        original_data = f.read()
    with open(
        os.path.splitext(filename)[0] + "receive" + os.path.splitext(filename)[1], "rb"
    ) as f:
        transferred_data = f.read()
    assert original_data == transferred_data, "File transfer failed"

    print("File transfer successful")


if __name__ == "__main__":
    test_file_transfer()
