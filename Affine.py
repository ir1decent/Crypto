def check_multiplicative_factor(factor):
    """
    判断乘法因子的限制条件
    """
    if factor < 0 or factor >= 26:
        return False
    elif factor % 2 == 0 or factor % 13 == 0:
        return False
    else:
        return True


def affine_encrypt(plaintext, multiplicative_factor, additive_factor):
    """
    仿射密码加密过程
    """
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            ascii_offset = ord("A") if char.isupper() else ord("a")
            encrypted_char = chr(
                (ord(char) - ascii_offset) * multiplicative_factor
                + additive_factor % 26
                + ascii_offset
            )
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext


def affine_decrypt(ciphertext, multiplicative_factor, additive_factor):
    """
    仿射密码解密过程
    """
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            ascii_offset = ord("A") if char.isupper() else ord("a")
            decrypted_char = chr(
                (
                    (ord(char) - ascii_offset - additive_factor)
                    * multiplicative_factor
                    % 26
                )
                + ascii_offset
            )
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext


multiplicative_factor = int(input("请输入乘法因子: "))
if check_multiplicative_factor(multiplicative_factor):
    plaintext = input("请输入明文: ")
    additive_factor = int(input("请输入加法因子: "))

    ciphertext = affine_encrypt(plaintext, multiplicative_factor, additive_factor)
    print("加密结果:", ciphertext)

    decrypted_text = affine_decrypt(ciphertext, multiplicative_factor, additive_factor)
    print("解密结果:", decrypted_text)
else:
    print("乘法因子不符合限制条件。")
