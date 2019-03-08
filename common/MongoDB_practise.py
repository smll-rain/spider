from pymongo import *

# 创建Mongoclient对象,"mongodb://用户名:密码@公网ip:端口/数据库名"
client = MongoClient('47.107.111.222', 27017)
#连接mydb数据库,账号密码认证
db = client.admin    # 先连接系统默认数据库admin
# 下面一条更改是关键，我竟然尝试成功了，不知道为啥，先记录下踩的坑吧
db.authenticate("python", "python", mechanism='MONGODB-CR') # 让admin数据库去认证密码登录，好吧，既然成功了，
# db.authenticate("python", "python")
db = client.test  # 再连接自己的数据库mydb
# 创建集合对象
stu = db.stu

# 查询
# 查询一条
doc = stu.find_one({'name':'test1017'})

# 查询多条
cursor = stu.find({'age': {'$lte': 50}})
for doc in cursor:
    print('%s---%s' % (doc.get('name'),doc.get('age')))

# # 添加
# # 插入1条
# stu.insert_one({'name':'xiaoming', 'age': 18})
#
# # 插入多条
# stu.insert_many({'name':'xiaosi', 'age': 18},
#                 {'name': 'xiaoli', 'age': 28},
#                 {'name': 'xiaowu', 'age': 38})
# # 修改
# # 修改1条
# stu.update_one({'name': 'xiaoming'}, {'$set':{'name': 'xiaosi'}})
#
# # 修改多条
# stu.update_many({'name': 'xiaosi'}, {'$set':{'name': 'xiaohong'}})
#
# # 删除
# # 删除1条
# stu.delete_one({'name': 'xiaowu'})
#
# # 删除多条
# stu.delete_many({'name': 'xiaosi'})