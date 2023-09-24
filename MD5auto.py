import hashlib


def calculate_md5(filename):
    with open(filename, "rb") as file:
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def verify_md5(filename, expected_md5):
    calculated_md5 = calculate_md5(filename)
    if calculated_md5 == expected_md5:
        print("MD5 verification passed.")
    else:
        print("MD5 verification failed. The calculated MD5 is:", calculated_md5)


# 示例用法
filename = "adult.data.txt"
expected_md5 = "098f6bcd4621d373cade4e832627b4f6"
md5 = calculate_md5(filename)
print("MD5 hash:", md5)
