import math as m
import numpy as np
import random
from pyope.ope import OPE, ValueRange
from scipy.spatial import KDTree
from scipy.spatial import distance


NUM = 10000000
STA = 1000000
# 加载二维乱序数据
int_data = []
with open("NE.txt", "r") as f:
    for line in f:
        x, y = line.strip().split(" ")
        int_data.append([int(float(x) * STA), int(float(y) * STA)])
# print(int_data[1])

# 加密数据
key = OPE.generate_key()
cipher = OPE(key, in_range=ValueRange(0, NUM))

encrypted_data = []
for d in int_data:
    encrypted_data.append([cipher.encrypt(int(d[0])), cipher.encrypt(int(d[1]))])

# 构建KD树索引
tree = KDTree(encrypted_data)


# 安全（近似）近邻查询
def secure_approximate_nearest_neighbors(query, k, eps):
    # 对查询数据进行加密
    encrypted_query = (cipher.encrypt(query[0]), cipher.encrypt(query[1]))

    # 计算查询半径(最大半径*eps)
    r = eps * tree.query(encrypted_query, k=k)[0][-1]
    # print(tree.query(encrypted_query, k=k))
    print("r:", r)

    # 构建查询矩形
    x_min = encrypted_query[0] - r
    x_max = encrypted_query[0] + r
    y_min = encrypted_query[1] - r
    y_max = encrypted_query[1] + r
    print("rectangle:", x_min, x_max, y_min, y_max)
    # 在KD树中查找查询矩形中的所有数据点
    indices = tree.query_ball_point([x_min, y_min], r=r * 1.5)
    indices += tree.query_ball_point([x_min, y_max], r=r * 1.5)
    indices += tree.query_ball_point([x_max, y_min], r=r * 1.5)
    indices += tree.query_ball_point([x_max, y_max], r=r * 1.5)
    indices = list(set(indices))  # 去重
    print("indices:", indices)
    # neighbors = [int_data[i] for i in indices]
    neighbors = [encrypted_data[i] for i in indices]

    # 计算加密距离
    encrypted_distances = [
        distance.euclidean(encrypted_query, [x, y])
        # [cipher.encrypt(x), cipher.encrypt(y)]
        for x, y in neighbors
    ]
    print(encrypted_distances)
    for i in neighbors:
        i[0] = cipher.decrypt(i[0])
        i[1] = cipher.decrypt(i[1])
        i[0] = i[0] / STA
        i[1] = i[1] / STA
    print("neighbors:", neighbors)
    # 排序并返回前k个近邻
    return [n for _, n in sorted(zip(encrypted_distances, neighbors))][:k]


# 示例查询
a, b = input("please input point:").split()
a = int(float(a) * STA)
b = int(float(b) * STA)
query = [a, b]
k = 5
eps = 0.5
# print(f"Query point: {query}")
print(
    f"Approximate nearest neighbors: {secure_approximate_nearest_neighbors(query, k, eps)}"
)
