import socket
import os
import random
import hashlib
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import time
import MD5
import RSA1
import json
import secrets
import base64
from Crypto.Random import get_random_bytes

p = 61
q = 53
public_keyS = (631, 3233)
private_keyS = (3031, 3233)
public_keyR = (2533, 3233)
private_keyR = (877, 3233)


# 生成密钥
"""def generate_key():
    return get_random_bytes(32)  # 32字节随机密钥"""


def generate_key():
    return hashlib.sha256(
        str(random.getrandbits(256)).encode("utf-8")
    ).digest()  # 32字节随机密钥


# 对文件进行AES加密
def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + ".enc"

    iv = os.urandom(16)  # 偏移量
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    filesize = os.path.getsize(in_filename)

    with open(in_filename, "rb") as infile:
        with open(out_filename, "wb") as outfile:
            outfile.write(filesize.to_bytes(8, byteorder="big"))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk = pad(chunk, 16)
                    # chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
                # print("read:",chunk.decode('utf-8','ignore'))
    print("-" * 40)
    return out_filename


# 对文件进行AES解密
def decrypt_file(key, in_filename, out_filename=None, chunksize=2 * 1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    else:
        out_filename = (
            os.path.splitext(out_filename)[0]
            + "receive"
            + os.path.splitext(out_filename)[1]
        )

    with open(in_filename, "rb") as infile:
        filesize = int.from_bytes(infile.read(8), byteorder="big")
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                # print(len(chunk))
                if len(chunk) == 0:
                    break
                if len(chunk) % 16 != 0:
                    chunk = pad(chunk, 16)
                out = outfile.write(decryptor.decrypt(chunk))
                # print(out)
                # print("receive:",chunk.decode('utf-8','ignore'))

            outfile.truncate(filesize)
    return out_filename


# 发送文件
def send_file(conn: socket.socket, in_filename):
    # key = "12345678901234567890129876543210".encode()
    key = generate_key()
    print(key)
    for byte in key:
        print(byte, end=", ")
    print(len(key))
    encrypted_key = RSA1.encrypt(public_keyR, key)
    md5 = MD5.calculate_md5(in_filename).encode("utf-8")
    print("生成摘要：", md5)
    encrypted_md5 = RSA1.encrypt(private_keyS, md5)
    print("数字签名：", encrypted_md5)
    # key = keys.encode()
    encrypted_filename = encrypt_file(key, in_filename)
    # encrypted_filename = in_filename
    filesize = os.path.getsize(encrypted_filename)
    pack = lambda data: struct.pack("!{}i".format(len(data)), *data)
    # conn.sendall(key)
    data = pack(encrypted_key)
    # print(len(data))
    conn.sendall(data)
    data = pack(encrypted_md5)
    # print(len(data))
    conn.sendall(data)
    # conn.send(encrypted_md5.encode())

    with open(encrypted_filename, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            conn.sendall(chunk)
            time.sleep(1)

    # os.remove(encrypted_filename)


# 接收文件
def receive_file(conn: socket.socket, out_filename):
    # time.sleep(5)
    # with open("key.txt", "rb") as keyfile:
    # encrypted_key = keyfile.read()
    # unencrypted_key = conn.recv(1024)
    encrypted_key = conn.recv(256)
    unpack = lambda data: struct.unpack(
        "!{}i".format(len(data) // struct.calcsize("i")), data
    )
    encrypted_key = unpack(encrypted_key)
    encrypted_md5 = conn.recv(256)
    encrypted_md5 = unpack(encrypted_md5)
    # with open("test.txt", "wb") as test:
    # test.write(key)
    # print(encrypted_key)
    # print(encrypted_md5)
    # print("解码：", encrypted_key)
    key = RSA1.decrypt(private_keyR, encrypted_key)
    print("解密后的密钥：", key)
    # for byte in key:
    #     print(byte, end=", ")
    # print(len(key))
    # print(key == encrypted_key)
    # encrypted_md5 = conn.recv(32)
    md5r = RSA1.decrypt(public_keyS, encrypted_md5).decode()
    print("解密后的摘要：", md5r)
    received_data = b""
    while True:
        data = conn.recv(8192)
        if not data:
            break
        received_data += data

    decrypted_filename = "received_file.enc"
    with open(decrypted_filename, "wb") as f:
        f.write(received_data)

    decrypt_file(key, decrypted_filename, out_filename)


# 服务端
def server(out_filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 1900
    s.bind((host, port))

    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("Connected by", addr)
        receive_file(conn, out_filename)
        conn.close()


# 客户端
def client(in_filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
    # s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
    host = "127.0.0.1"
    port = 1900

    s.connect((host, port))

    send_file(s, in_filename)
    time.sleep(3)

    s.close()
