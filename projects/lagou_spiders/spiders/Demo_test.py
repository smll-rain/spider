# coding:utf-8
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 用于正常显示中文标签
plt.rcParams["font.sans-serif"]=['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False
fig = plt.figure()
fig.suptitle('没有子图的情况')
fig, ax = plt.subplots(2, 2)
plt.show()