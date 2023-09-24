def is_coprime(a, b):
    while b:
        a, b = b, a % b
    return a == 1


def multiplicative_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def encrypt(plaintext, key):
    a, b = key
    if not is_coprime(a, 26):
        raise ValueError("乘法因子必须与模数26互质。")
    ciphertext = ""
    for c in plaintext:
        if c.isalpha():
            if c.islower():
                new_char = chr((a * (ord(c) - ord("a")) + b) % 26 + ord("a"))
            else:
                new_char = chr((a * (ord(c) - ord("A")) + b) % 26 + ord("A"))
            ciphertext += new_char
        else:
            ciphertext += c
    return ciphertext


def decrypt(ciphertext, key):
    a, b = key
    a_inv = multiplicative_inverse(a, 26)
    if a_inv is None:
        raise ValueError("乘法因子的逆元不存在。")
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            if c.islower():
                new_char = chr((a_inv * (ord(c) - ord("a") - b)) % 26 + ord("a"))
            else:
                new_char = chr((a_inv * (ord(c) - ord("A") - b)) % 26 + ord("A"))
            plaintext += new_char
        else:
            plaintext += c
    return plaintext


# 测试加解密
plaintext = "hello world"
key = (5, 8)  # (乘法因子, 加法因子)
try:
    ciphertext = encrypt(plaintext, key)
    print("密文：", ciphertext)
    decrypted_text = decrypt(ciphertext, key)
    print("解密后的明文：", decrypted_text)
except ValueError as e:
    print("错误：", str(e))


"""仿射密码是一种替换密码。它是一个字母对一个字母的。

它的加密函数是e(x)=ax+b(mod m)，其中a和m互质。

m是字母的数目。

解码函数是d(x)=a-1(x-b)，其中a-1是在群Zm的乘法逆元。"""
