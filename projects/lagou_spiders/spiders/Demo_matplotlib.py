# coding:utf-8
import matplotlib.pyplot as plt
import numpy as np

# 对数坐标图
w = np.linspace(0.1, 1000, 1000)
p = np.abs(1/(1+0.1j*w)) # 计 算 低 通 滤 波 器 的 频 率 响 应
fig, axes = plt.subplots(2, 2)
functions = ("plot", "semilogx", "semilogy", "loglog")
for ax, fname in zip (axes.ravel(), functions):
    func = getattr(ax, fname)
    func(w, linewidth=2)

# 极坐标图
theta = np.arange(0, 2*np.pi, 0.02)
plt.subplot(121, polar=True)
plt.plot(theta, 1.6*np.ones_like(theta), lw=2)
plt.plot(3*theta, theta/3, '--', lw=2)

plt.subplot(122, polar=True)
plt.plot(theta, 1.4*np.cos(5*theta), '--', lw=2)
plt.plot(theta, 1.8*np.cos(4*theta), lw=2)
plt.rgrids(np.arange(0.5, 2, 0.5), angle=45)
plt.thetagrids([0, 45])
plt.show()


# 堆叠柱状图
name_list = ['Monday', 'Tuesday', 'Friday', 'Sunday']
num_list = [1.5, 0.6, 7.8, 6]
num_list1 = [1, 2, 3, 1]
plt.bar(range(len(num_list)), num_list, width=0.5, label='boy', fc='c')
plt.bar(range(len(num_list)), num_list1, width=0.5, bottom=num_list, label='girl', tick_label=name_list, fc='r')
plt.legend()
plt.show()

# 并列柱状图
name_list = ['Monday', 'Tuesday', 'Friday', 'Sunday']
num_list = [1.5, 0.6, 7.8, 6]
num_list1 = [1, 2, 3, 1]
x = list(range(len(num_list)))
total_width, n = 0.8, 2
width = total_width / n

plt.bar(x, num_list, width=width, label='boy', fc='c')
# 利用柱状图的宽度，将其分隔开，如果不分隔，则会编程堆叠柱状图
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list1, width=width, label='girl', tick_label=name_list, fc='m')
plt.legend()
plt.show()

# 条形柱状图
# -*- coding: utf-8 -*-
name_list = ['Monday', 'Tuesday', 'Friday', 'Sunday']
num_list = [1.5, 0.6, 7.8, 6]
plt.barh(range(len(num_list)), num_list, height=0.5, tick_label=name_list, color=['g', 'r', 'c', 'm', 'y', 'k', 'w'])
plt.show()


# 倒影柱状图
# -*- coding: utf-8 -*-
n = 12
X = np.arange(n)
# np.random.uniform(0.5, 1.0, n) 在[0.5 1.0)随机生成n个浮点数
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

# 为柱状图添加高度值
for x, y in zip(X, Y1):
    # ha: 横向对齐方式
    # va: 纵向对齐方式
    #  '%.2f' % y传入数保留两位小数
    plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

for x, y in zip(X, Y2):
    plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

plt.xlim(-.5, n)
plt.xticks(())
plt.ylim(-1.25, 1.25)
plt.yticks(())

plt.show()
