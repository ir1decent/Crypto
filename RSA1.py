import random
from typing import ByteString, List
from Crypto.Util.number import getPrime


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_keypair(p, q):
    # 生成公钥和私钥
    n = p * q
    phi = (p - 1) * (q - 1)

    # 选择一个与 phi 互质的整数 e
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # 计算 e 在模 phi 下的乘法逆元
    d = mod_inverse(e, phi)

    return ((e, n), (d, n))


def mod_inverse(a, m):
    # 计算 a 在模 m 下的乘法逆元
    _, x, _ = extended_gcd(a, m)
    return x % m


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def encrypt(private_key, plaintext: bytes):
    # 加密明文
    e, n = private_key
    ciphertext = list()
    for char in plaintext:
        ciphertext.append(pow(int(char), e, n))
        # print(len(ciphertext))
    return ciphertext


def decrypt(public_key, ciphertext: List[int]):
    # 解密密文
    d, n = public_key
    plaintext = list()
    for int_val in ciphertext:
        plaintext.append(pow(int_val, d, n))
        # print(pow(int_val, d, n), end=", ")
    return bytes(plaintext)


# 生成密钥对
# prime = getPrime(bit_length)
# print(prime)
# p = 61
# q = 53
# public_key, private_key = generate_keypair(p, q)

# # 加密和解密示例
# message = "c69d2b31cea5de5f60d2b787bbfb8b8a".encode()
# encrypted_message = encrypt(public_key, message)
# decrypted_message = decrypt(private_key, encrypted_message)

# print("公钥:", public_key)
# print("私钥:", private_key)
# print("加密后:", encrypted_message)
# print("解密后:", decrypted_message)
