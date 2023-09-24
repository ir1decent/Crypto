import numpy as np
import pandas as pd
import csv
from numpy.random import laplace
import copy
import matplotlib.pyplot as plt

# 配置信息
# 数据集文件路径
censusData_FilePath = "adult.data.txt"
# 属性标签
attributeLabels = [
    "age",  # 0年龄            int64
    "workclass",  # 1工作类型        object
    "fnlwgt",  # 2人口特征权重    int64
    "education",  # 3学历            object
    "education_num",  # 4受教育时间      int64
    "marital_status",  # 5婚姻状态        object
    "occupation",  # 6职业            object
    "relationship",  # 7关系            object
    "race",  # 8种族            object
    "sex",  # 9性别            object
    "capital_gain",  # 10资本收益        int64
    "capital_loss",  # 11资本损失        int64
    "hours_per_week",  # 12每周工作小时数  int64
    "native_country",  # 13原籍            object
    "wage_class",  # 14收入类别        object
]


# 准标识符
quasi_identifier_list = []
quasi_identifier_DGH_list = []
quasi_identifier_VGH_list = []
quasi_identifier_height_list = []
# marital-status属性标签
workclass_attributeLabels = [
    "***",  # 0抑制标签
    "Private-h2",  #
    "Non-Private",  #
    "Private-h1",  #
    "government department",  #
    "Self-employed",  #
    "Private",  #
    "Self-emp-not-inc",  #
    "Self-emp-inc",  #
    "Federal-gov",  #
    "Local-gov",  #
    "State-gov",  #
    "Without-pay",
    "Never-worked",
]
# workclass的泛化树
vgh_marital = pd.DataFrame(
    {
        "value": workclass_attributeLabels,
        "parent": [-1, 0, 0, 1, 2, 2, 3, 5, 5, 4, 4, 4, 5, 5],
        "height": [3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    }
)

quasi_identifier_list.append(attributeLabels[1])  # 将workclass设置为准标识符
quasi_identifier_DGH_list.append(3)
quasi_identifier_VGH_list.append(vgh_marital)
quasi_identifier_height_list.append(0)

# print(vgh_marital)
# race属性标签
race_attributeLabels = [
    "***",  # 抑制标签
    "White-h1",  
    "Non-White",  
    "White",  
    "Asian-Pac-Islander",  
    "Amer-Indian-Eskimo",  
    "Other",  
    "Black",  
]
# race的泛化树
vgh_race = pd.DataFrame(
    {
        "value": race_attributeLabels,
        "parent": [-1, 0, 0, 1, 2, 2, 2, 2],
        "height": [2, 1, 1, 0, 0, 0, 0, 0],
    }
)

quasi_identifier_list.append(attributeLabels[8])  # 将race设置为准标识符
quasi_identifier_DGH_list.append(2)
quasi_identifier_VGH_list.append(vgh_race)
quasi_identifier_height_list.append(0)

# print(vgh_race)
# marital-status属性标签
marital_attributeLabels = [
    "***",  # 抑制标签
    "Married-h2",  
    "Alone",  
    "Married-h1",  
    "Single",  
    "Widowhood",  
    "Married-civ-spouse", 
    "Married-AF-spouse",  
    "Separated",  
    "Divorced",  
    "Never-married",  
    "Widowed",  
    "Married-spouse-absent",  
]
# marital-status的泛化树
vgh_marital = pd.DataFrame(
    {
        "value": marital_attributeLabels,
        "parent": [-1, 0, 0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5],
        "height": [3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    }
)

quasi_identifier_list.append(attributeLabels[5])  # 将marital-status设置为准标识符
quasi_identifier_DGH_list.append(3)
quasi_identifier_VGH_list.append(vgh_marital)
quasi_identifier_height_list.append(0)



# 导入数据集
censusData_SetFull = pd.read_csv(censusData_FilePath, names=attributeLabels)

# 将缺失值部分的“ ？” 置为空，即 np.NaN，便于使用pandas来处理缺失值
censusData_SetFull = censusData_SetFull.replace(" ?", np.NaN)

# 类型为字符串的标签
attributeLabels_str = [
    "workclass",
    "education",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native_country",
    "wage_class",
]
# 删除数据值前的空格
for label in attributeLabels_str:
    censusData_SetFull[label] = censusData_SetFull[label].str.strip()

# 删除包含缺失值的行
censusData_SetFull.dropna(inplace=True)
# 重置索引
censusData_SetFull.reset_index(drop=True, inplace=True)
censusData_Set = copy.deepcopy(censusData_SetFull)


# 年龄处理
def age_k_anonymize(data, k):
    data["age"] = data["age"].astype(float)
    # 对年龄进行分组
    data["age"] = pd.cut(data["age"], bins=k)
    # 对敏感属性进行泛化处理
    data["age"] = data.groupby("age")["age"].transform(lambda x: np.random.choice(x))
    return data


# 检验是否满足k匿名
# 将所有准标识符的组合存入字典，值为出现次数。
def group_data(testedSet):
    quasiDict = {}
    # q = 0
    for item in testedSet.itertuples():
        # 将准标识符转化为字符串
        item_statement = ""
        for label in quasi_identifier_list:
            item_statement = item_statement + getattr(item, label) + " "
        # 如果该准标识符组合已经出现过了，则计数+1
        if item_statement in quasiDict.keys():
            quasiDict[item_statement] += 1
            # q += 1
        # 如果该准标识符组合没有出现过，则新建记录
        else:
            quasiDict[item_statement] = 1
            # q += 1
    # 返回字典
    # print(q)
    return quasiDict


# 判断数据集testedSet是否满足k匿名，是则返回true，否则返回false
def if_k(testSet, k):
    # 对数据集进行分组，获得组合数量
    ans_dict = group_data(testSet)
    age_counts = testSet.groupby("age")["age"].count()
    min_count = age_counts.min()
    if min_count < k:
        print("K-匿名要求未满足，最小频数为:", min_count)
    # 展示准标识符组合
    print("")
    print(ans_dict)
    print("")
    min_k = None
    # 遍历分组字典，取出最小的重复个数，赋值给min_k
    for i in ans_dict:
        if min_k is None or ans_dict[i] < min_k:
            min_k = ans_dict[i]
    # 如果字典的最小k值大于等于给定的k值，则满足k匿名
    if min_k >= k:
        return True
    else:
        return False


# 对数据集tempDataSet（dataframe）的属性列attr（String）进行泛化
# vgh（dataframe）是泛化树
def Generalization_attr(tempDataSet, attr, vgh, h):
    for index, row in vgh.iterrows():
        if row.height == h:
            tempDataSet.replace(
                {attr: row.value}, vgh.loc[row.parent].value, inplace=True
            )


# 演示取值：16000；2；15；140
k_Anonymity = 10

censusData_Set = age_k_anonymize(censusData_Set, k_Anonymity)

# 泛化次数计数，初始化为所有准标识符泛化次数之和
gen_count = 0
for index in range(len(quasi_identifier_DGH_list)):
    gen_count += quasi_identifier_DGH_list[index]


while if_k(censusData_Set, k_Anonymity) is False:
    for index in range(len(quasi_identifier_list)):
        # 如果已经到达了泛化顶点
        if quasi_identifier_height_list[index] >= quasi_identifier_DGH_list[index]:
            continue
        # 泛化
        Generalization_attr(
            censusData_Set,
            quasi_identifier_list[index],
            quasi_identifier_VGH_list[index],
            quasi_identifier_height_list[index],
        )
        # 泛化次数-1
        gen_count -= 1
        # 泛化高度+1
        quasi_identifier_height_list[index] += 1
        if if_k(censusData_Set, k_Anonymity):
            break
    print("当前泛化高度：")
    for index in range(len(quasi_identifier_list)):
        print(
            quasi_identifier_list[index]
            + ":"
            + str(quasi_identifier_height_list[index])
        )
    # 直至无法泛化
    if gen_count == 0:
        print("泛化失败")
        break

print("当前泛化高度：")
for index in range(len(quasi_identifier_list)):
    print(quasi_identifier_list[index] + ":" + str(quasi_identifier_height_list[index]))

print("当前k值为：")
print(k_Anonymity)
# print("精确度为：")
prec = 0
for index in range(len(quasi_identifier_list)):
    prec += (quasi_identifier_height_list[index]) / (quasi_identifier_DGH_list[index])
prec = 1 - (prec / len(quasi_identifier_list))

# print(prec)
# 删除"wage_class"列
censusData_Set = censusData_Set.drop("wage_class", axis=1)
censusData_Set = censusData_Set.drop("fnlwgt", axis=1)

# 将数据保存为文本文件
censusData_Set.to_csv("data.txt", index=False, sep="\t")
selected_columns = ["age", "workclass", "marital_status", "race"]
data_selected = censusData_Set[selected_columns]

# 将处理后的数据保存为文本文件
data_selected.to_csv("data_selected.txt", index=False, sep="\t")

data_selected["age"] = data_selected["age"].apply(lambda x: (x.mid))
k_average_age = data_selected["age"].mean()
print("K匿名后平均年龄：", k_average_age)
# 计算差分隐私参数
epsilon = 1.0  # 差分隐私参数
sensitivity = 1.8  # 年龄的灵敏度

# 添加拉普拉斯噪声
laplace_noise = laplace(scale=sensitivity / epsilon, size=len(data_selected))
dp_k_anonymized_data = data_selected.copy()
dp_k_anonymized_data["age"] += laplace_noise

# 计算差分隐私发布后的平均年龄
dp_average_age = dp_k_anonymized_data["age"].mean()
print("差分隐私发布后的平均年龄:", dp_average_age)

# 将k-匿名和差分隐私后的数据保存到文件
dp_k_anonymized_data.to_csv("dp_k_anonymized_data.txt", index=False)

# 删除某条数据后的影响
censusData_SetFull["age"] = censusData_SetFull["age"].astype(float)
index_to_delete = 1  # 假设要删除的数据的索引为0
k_anonymized_data_deleted = data_selected.drop(index_to_delete)
# print(censusData_SetFull)
real_age_data_deleted = censusData_SetFull.drop(index_to_delete)
dp_k_anonymized_data_deleted = dp_k_anonymized_data.drop(index_to_delete)
real_age_average = censusData_SetFull["age"].mean()
print("原数据平均年龄：", real_age_average)
print(
    "K匿名后平均年龄可用性:",
    1 - np.abs(k_average_age - real_age_average) / real_age_average,
)
print(
    "差分隐私后平均年龄可用性:",
    1 - np.abs(dp_average_age - real_age_average) / real_age_average,
)
# 计算删除数据后的平均年龄
k_anonymized_average_age_deleted = k_anonymized_data_deleted["age"].mean()
# print(k_anonymized_average_age_deleted)
real_age_average_deleted = real_age_data_deleted["age"].mean()
# print(real_age_average_deleted)
dp_average_age_deleted = dp_k_anonymized_data_deleted["age"].mean()
# print(dp_average_age_deleted)
k_canuse = 1 - np.abs(k_average_age - real_age_average) / real_age_average
dp_canuse = 1 - np.abs(dp_average_age - real_age_average) / real_age_average

# 分析隐私信息泄露的可能性（使用L1距离）
privacy_leakage_real = np.abs(real_age_average - real_age_average_deleted)
privacy_leakage_k_anonymized = (
    np.abs(k_average_age - k_anonymized_average_age_deleted)
) * k_canuse
privacy_leakage_dp = np.abs(dp_average_age - dp_average_age_deleted) * dp_canuse
print("隐私信息泄露的可能性:", privacy_leakage_real)
print("隐私信息泄露的可能性- K匿名发布:", privacy_leakage_k_anonymized)
print("隐私信息泄露的可能性- 差分隐私发布:", privacy_leakage_dp)


# 绘制数据集年龄分布
plt.hist(censusData_SetFull["age"], bins=20, alpha=0.3, label="Original")
plt.hist(data_selected["age"], bins=20, alpha=0.3, label="K-Anonymized")
plt.hist(dp_k_anonymized_data["age"], bins=20, alpha=0.3, label="Noisy")
plt.legend()
plt.show()
