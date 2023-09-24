import numpy as np
import pandas as pd


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
    "***",  # 0抑制标签
    "White-h1",  # 1白人
    "Non-White",  # 2非白人
    "White",  # 3白人
    "Asian-Pac-Islander",  # 亚洲-太平洋-伊斯兰人
    "Amer-Indian-Eskimo",  # 美洲-印第安人-爱斯基摩人
    "Other",  # 其他
    "Black",  # 黑人
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
    "***",  # 0抑制标签
    "Married-h2",  # 1已婚
    "Alone",  # 2独自一人
    "Married-h1",  # 3已婚
    "Single",  # 4单身
    "Widowhood",  # 5鳏寡
    "Married-civ-spouse",  # 已婚-公民-配偶
    "Married-AF-spouse",  # 已婚-无房-配偶
    "Separated",  # 分居
    "Divorced",  # 离婚
    "Never-married",  # 未婚
    "Widowed",  # 寡居
    "Married-spouse-absent",  # 已婚-配偶-不在
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

# print(vgh_marital)
# 年龄属性标签
age_attributeLabels = [
    "***",  # 0抑制标签
    "0-20",  # 1年龄区间 0-20岁
    "21-40",  # 2年龄区间 21-40岁
    "41-60",  # 3年龄区间 41-60岁
    "61-80",  # 4年龄区间 61-80岁
    "81+",  # 5年龄区间 91岁以上
]
# age的泛化树
vgh_age = pd.DataFrame(
    {
        "value": age_attributeLabels,
        "parent": [-1, 0, 0, 0, 0, 0],
        "height": [1, 0, 0, 0, 0, 0],
    }
)

quasi_identifier_list.append(attributeLabels[0])  # 将age设置为准标识符
quasi_identifier_DGH_list.append(1)
quasi_identifier_VGH_list.append(vgh_age)
quasi_identifier_height_list.append(0)

# 导入数据集
censusData_Set = pd.read_csv(censusData_FilePath, names=attributeLabels)

# 将缺失值部分的“ ？” 置为空，即 np.NaN，便于使用pandas来处理缺失值
censusData_Set = censusData_Set.replace(" ?", np.NaN)

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
    censusData_Set[label] = censusData_Set[label].str.strip()

# 删除包含缺失值的行
censusData_Set.dropna(inplace=True)
# 重置索引
censusData_Set.reset_index(drop=True, inplace=True)
# 检验是否满足k匿名


# 将所有准标识符的组合存入字典，值为出现次数。
def group_data(testedSet):
    quasiDict = {}
    #q = 0
    for item in testedSet.itertuples():
        # 将准标识符转化为字符串
        item_statement = ""
        for label in quasi_identifier_list:
            item_statement = item_statement + getattr(item, label) + " "
        # 如果该准标识符组合已经出现过了，则计数+1
        if item_statement in quasiDict.keys():
            quasiDict[item_statement] += 1
            #q += 1
        # 如果该准标识符组合没有出现过，则新建记录
        else:
            quasiDict[item_statement] = 1
            #q += 1
    # 返回字典
    #print(q)
    return quasiDict


# 判断数据集testSet是否满足k匿名，是则返回true，否则返回false
def if_k(testedSet, k):
    # 对数据集进行分组，获得组合数量
    ans_dict = group_data(testedSet)
    # -----------------------------------------------------------------
    # 展示准标识符组合
    print("")
    print(ans_dict)
    print("")
    # -----------------------------------------------------------------
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
k_Anonymity = 15

# 泛化次数计数，初始化为所有准标识符泛化次数之和
gen_count = 0
for index in range(len(quasi_identifier_DGH_list)):
    gen_count += quasi_identifier_DGH_list[index]


while if_k(censusData_Set, k_Anonymity) is False:
    for index in range(len(quasi_identifier_list)):
        # 如果已经到达了泛化顶点
        if quasi_identifier_height_list[index] >= quasi_identifier_DGH_list[index]:
            continue
        # -----------------------------------------------------------------
        # 泛化
        Generalization_attr(
            censusData_Set,
            quasi_identifier_list[index],
            quasi_identifier_VGH_list[index],
            quasi_identifier_height_list[index],
        )
        # -----------------------------------------------------------------
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
#print("精确度为：")
prec = 0
for index in range(len(quasi_identifier_list)):
    prec += (quasi_identifier_height_list[index]) / (quasi_identifier_DGH_list[index])
prec = 1 - (prec / len(quasi_identifier_list))

#print(prec)