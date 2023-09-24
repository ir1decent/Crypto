def encrypt(plaintext, key):
    ciphertext = ""
    for c in plaintext:
        if c.isalpha():
            shift = ord("a") if c.islower() else ord("A")
            new_char = chr((ord(c) - shift + key) % 26 + shift)
            ciphertext += new_char
        else:
            ciphertext += c
    return ciphertext


def decrypt(ciphertext, key):
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            shift = ord("a") if c.islower() else ord("A")
            new_char = chr((ord(c) - shift - key) % 26 + shift)
            plaintext += new_char
        else:
            plaintext += c
    return plaintext


# 测试加解密
plaintext = "hello world"
key = 3
print("key=", key)
ciphertext = encrypt(plaintext, key)
print("密文：", ciphertext)
decrypted_text = decrypt(ciphertext, key)
print("解密后的明文：", decrypted_text)
