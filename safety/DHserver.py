import socket
import random as r
import math as m


def isPrime(p):
    if p <= 1:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i = i + 1
    return True


# while(1):
# a=int(input())
# print(isPrime(a))


def get_generator(p):
    j = 2
    list = []
    while j < p:
        flag = 1
        while flag != p:
            if (j**flag) % p == 1:
                break
            flag += 1
        if flag == (p - 1):
            list.append(j)
        j += 1
    return list


def get_cal(p, g, Random):
    K = (g**Random) % p
    return K


def get_key(Random, K, p):
    key = (K**Random) % p
    return key


def Server(x):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 51891
    socket_server.bind((host, port))
    socket_server.listen(5)
    client_socket, address = socket_server.accept()
    recv_m = client_socket.recv(1024)
    if recv_m != "\0":
        print("接收到客户端数据：%s" % recv_m.decode("utf-8"))
    send_m = x
    client_socket.send(str(send_m).encode("utf-8"))
    socket_server.close()
    return recv_m


while 1:
    p = int(input("请输入素数："))
    if isPrime(p) == False:
        print("非素数，请重新输入！")
    else:
        break


def encrypt(msg, key):
    encrypted = ""
    for char in msg:
        encrypted += chr((ord(char) + key) % 256)
        key = (key + 1) % 256
    return encrypted


if __name__ == "__main__":
    print("服务端正在运行：")
    p = 1999
    list = get_generator(p)
    Rb = r.randint(0, p - 1)  # 随机
    Kb = get_cal(p, int(list[-1]), Rb)
    Ka = int(Server(Kb))
    key_b = get_key(Rb, Ka, p)
    print("服务端生成密钥：%d" % key_b)
    judge_b = int(Server(key_b))
    if judge_b == key_b:
        print("比对成功")
    plaintext = "Hello, world!"
    ciphertext = encrypt(plaintext, key_b)
    Server(ciphertext)
    print("Ciphertext:", ciphertext)
