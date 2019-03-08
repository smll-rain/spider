import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 1000)  # x坐标范围
y = np.sin(x)
z = np.cos(x ** 2)
# 创建一个图表对象， 若不创建，matplotlib会自动创建， figsize指定对象figure对象的宽度和高度， 单位英寸
# dpi参数可以指定图像的分辨率，默认使用100，示例中所创建的Figure对象的宽度为8*100 = 800个像素。
plt.figure(figsize=(10, 4))

# x坐标，y坐标， label线条标注， color线条颜色，linewidth线条粗细
# 实际上plot()实在Axes(子图)对象上绘图，如果当前没有Axes对象，将会创建一个几乎充满整个图表的Axes对象，并且成为当前的Axes对象
# plot()前两个参数是X、Y轴数据的对象
# 第三个参数'b--'指定曲线的颜色和线性，b表示蓝色，'--'表示虚线， Ipython中输入plt.plot？可以查看格式化字符串以及各个参数说明
# label参数给曲线指定一个标签， 如果标签字符串前后有字符“$”,matplotlib会使用内嵌的LaTeX引擎将其显示为数学公式
# 使用LaTeX语法绘制数学公式会极大地降低图表的描绘速度
# color指定曲线的颜色，可以是英文单词、#字符开头的16位进制数表示"#ffffff"、0到1之内的三个元素元素表示（1.0，0.0，0.0）红色
# linewidth 指定曲线的宽度，可以不是整数，可以写成缩写参数名lw
plt.plot(x, y, label='$sin(x)$', color="red", linewidth=2)
plt.plot(x, z, 'b--', label='$cos(x^2)$', linewidth=2)
plt.xlabel('Time(s)')  # x轴标注
plt.ylabel('Volt')  # y轴标注
plt.title('PyPlot First Example')  # 表题
# xlim、ylim分别设置X/Y轴的显示范围
plt.ylim(-1.0, 1.0)  # y坐标范围
plt.legend()  # 显示图示，即图中表示每条曲线的标签(label)和样式的矩形区域
plt.savefig('test.png', dpi=1000)  # 可以通过此方法编写批量输入图表，需放在plt.show()之前执行
plt.show()  # 显示绘图窗口， 会阻塞程序的运行，直到画图结束

# 获取图表对象
fig = plt.gcf()  # 获取Figure对象
axes = plt.gca()  # 获取Axes对象
print(fig)
print(axes)

# 配置属性  对象的set_*()方法或者pyplot模块的setp()设置
fig = plt.figure()
fig.set(alpha=0.2)  # alpha设置图像的透明度
x = np.arange(0, 1, 0.1)
line = plt.plot(x, 0.5 * x * x)[0]  # plot返回一个列表
line.set_alpha(0.5)
lines = plt.plot(x, np.sin(x), x, np.cos(x))
plt.setp(lines, color='r', lw=4)

# 获取对象属性
print(line.get_linewidth())
print(plt.getp(lines[0], "color"))
# 获取对象所有属性
plt.getp(lines)
plt.show()

# 绘制多子图 plt.subplot(numRows, numCols, plotNum) 整个图表分为numRows行，numCols列
# 按照从左到右，从上到下的顺序对每个区域进行编号，左上区域的编号为1
# plotNum指定所创建的Axes对象的区域
# 如果三个参数都小于10 ，可以将其缩写为一个整数，如subplot(323), 与subplot(3, 2, 3)相同
# 如果创建的子图区域有重叠的部分，之前的子图将被删除
# facecolor设置子图背景
for idx, color in enumerate('rgbyck'):
    plt.subplot(321 + idx, facecolor=color)
plt.show()

# 占据整列
plt.subplot(331, facecolor="r")

# 占据整行
plt.subplot(313, facecolor="b")
plt.show()

# 调节子图间距和边距
# plt.subplots_adjust(left, right, top, bottom, wspace, hspace)
# 切换图表
# subplot()返回所创建的Axes对象，可以通过sca()切换对象
plt.figure(1)
plt.figure(2)
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)
x = np.linspace(0, 3, 100)
for i in range(5):
    plt.figure(1)
    plt.plot(x, np.exp(i * x / 3))
    plt.sca(ax1)
plt.show()

# 表格布局 subplot2grid(shape, loc, rowspan=1, colspan=1, **kwargs)
# shape表示表格形状的元祖(行数，列数)，loc为子图左上角所在的坐标：(行, 列)
# rowspan和colspan分别为子图所占据的行数和列数
fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
ax2 = plt.subplot2grid((3, 3), (0, 2), rowspan=2)
ax3 = plt.subplot2grid((3, 3), (1, 0), rowspan=2)
ax4 = plt.subplot2grid((3, 3), (2, 1), colspan=2)
ax5 = plt.subplot2grid((3, 3), (1, 1))
plt.show()

# 配置文件   可以使用多个matplotlibrc配置文件，顺序靠前的配置文件会被优先采用
# 搜索顺序如下：当前路径-->用户配置路径(通常在.matplotlib目录下)-->系统配置路径
# 获取用户配置路径
from os import path
import matplotlib
# 获取当前配置路径
current_path = path.abspath(matplotlib.matplotlib_fname())
print(current_path)
# 读取配置文件配置内容， 本质上是一个字典
print(matplotlib.rc_params())

# 修改配置信息
matplotlib.rc("lines", marker="x", lw=2, color="red")

# 配置恢复默认
matplotlib.rcdefaults()

# 手工修改配置后，重新载入最新配置
matplotlib.rcParams.update(matplotlib.rc_params())

# 获取用户配置路径
user_path = path.abspath(matplotlib.get_configdir())
print(user_path)

# 样式切换  matplotlib.style
from matplotlib import style
# 获得可选样式
print(style.available)
# 切换样式
style.use("ggplot")

# 在图表中显示中文， 默认无法显示中文
# 在程序中直接指定字体。
# 在程序开头修改配置字典rcParams。
# 修改配置文件
# 获取所有可用字体列表, ttflist是matplotlib的系统字体列表
from matplotlib.font_manager import fontManager
print(fontManager.ttflist[:])
# 字体名称
print(fontManager.ttflist[0].name)
# 字体路径
print(fontManager.ttflist[0].fname)

# 设置显示字体
plt.rcParams['font.sans-serif']=['SimHei']
