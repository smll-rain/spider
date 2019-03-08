# coding:utf-8
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
df = pd.read_csv(r'../../analysis_positions_20181204.csv', encoding='utf-8')
# print(df.head())
print(df.describe())
# print(df.dtypes)
# print(df.shape)
# print(df.columns)
# print(df.columns.name)
# print(df.index)
# print(df.index.names)


plt.rcParams['font.sans-serif']=['SimHei'] #指定默认字体 SimHei为黑体, 解决标签显示乱码问题
# # 计算每列的均值
# print(df.mean())
# # 计算每行的均值
# print(df.mean(axis=1))

# fig = plt.figure()
# fig.set(alpha=0.2)

# 用于正常显示中文标签
plt.rcParams["font.sans-serif"]=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False
# 乘客等级分布
plt.figure() # 在一张大图里分列几个小图
# df.workYear.value_counts().plot(kind='bar',)  # 柱状图
x = df.workYear.value_counts().index
y = df.workYear.value_counts().values
rects = plt.bar(x, y,width=0.5, color=['g', 'r', 'c', 'm', 'y', 'k', 'w'])
for rect in rects:
    x1 = rect.get_x() + 0.1
    height = rect.get_height()
    plt.text(x1, height * 1.02, str(height) + '个')

plt.title(u'2018年11-12月数据分析职位统计(按工作年限统计)')  # 标题
plt.xlabel(u'工作年限')
plt.ylabel(u'岗位数')
# 开启网格线
# plt.grid(True)
plt.savefig('2018年11-12月数据分析职位统计(按工作年限统计).png')
plt.show()




