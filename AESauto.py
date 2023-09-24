from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


def generate_key():
    return get_random_bytes(16)  # 生成一个随机的16字节（128位）密钥


def encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_CBC)  # 使用CBC模式加密
    cipher_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")  # 将初始化向量编码为Base64字符串
    cipher_text = b64encode(cipher_text).decode("utf-8")  # 将密文编码为Base64字符串
    return iv, cipher_text


def decrypt(iv, cipher_text, key):
    iv = b64decode(iv.encode("utf-8"))  # 将Base64字符串解码为字节串
    cipher_text = b64decode(cipher_text.encode("utf-8"))  # 将Base64字符串解码为字节串
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return plain_text.decode("utf-8")


# 示例用法
key = generate_key()
plain_text = "Hello, AES!"
iv, cipher_text = encrypt(plain_text, key)
decrypted_text = decrypt(iv, cipher_text, key)

print("Plaintext:", plain_text)
print("Cipher Text:", cipher_text)
print("Decrypted Text:", decrypted_text)
