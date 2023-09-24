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


def Client(x):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 51891
    client.connect((host, port))
    send_m = x
    client.send(str(send_m).encode("utf-8"))
    recv_m = client.recv(1024)
    if recv_m != "\0":
        print("接收到服务器数据：%s" % recv_m.decode("utf-8"))
    client.close()
    return recv_m


# while(1):
# p=int(input("请输入素数："))
# if(isPrime(p)==False):
# print("非素数，请重新输入！")
# else:
# break


def decrypt(msg, key):
    decrypted = ""
    for char in msg:
        decrypted += chr((ord(char) - key) % 256)
        key = (key + 1) % 256
    return decrypted


if __name__ == "__main__":
    print("客户端正在运行：")
    p = 1999  # 约定素数
    list = get_generator(p)  # 获得原根(g)
    Ra = r.randint(0, p - 1)
    Ka = get_cal(p, int(list[-1]), Ra)
    Kb = int(Client(Ka))
    key_a = get_key(Ra, Kb, p)
    print("客户端生成密钥：%d" % key_a)
    judge_a = int(Client(key_a))
    if judge_a == key_a:
        print("比对成功")
    ciphertext = str(Client(0).decode("utf-8"))
    print("接收到的密文：", ciphertext)
    decrypted_text = decrypt(ciphertext, key_a)
    print("解密:", decrypted_text)
