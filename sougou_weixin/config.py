# -*- coding: utf-8 -*-
# author: Right.Hai
# time: 2019/04/11
# email: 1955507077@qq.com
# for: 配置文件

# 需要搜索的关键字
KEY = 'python'
# cookie需要自己登陆网站手动复制
COOKIES = '',

"""
MySQL数据库配置, 
需要在数据库先创建数据库，表里面字段如下：
id(自增),title,content,date,wechat,'nickname'
"""
# 地址
MYSQL_HOST = ''
# 端口
MYSQL_PORT = 'your_port'
# 用户名
MYSQL_USER = ''
# 密码
MYSQL_PASSWORD = ''
# 数据库， 需要先创建
MYSQL_DATABASE = ''

"""
Redis数据库配置
"""
# redis端口
REDIS_PORT = 'your_port'
# redis 地址
REDIS_HOST = ''
# redis密码
REDIS_PWD = ''
# redis 存储的键
REDIS_KEY = ''

# 成功状态码
VALID_STATUS = [200]
# 获取代理的地址，返回的ip结果如：ip:port, 类型为字符串str
PROXY_URL = ''
# 最大失败重试次数
MAX_FAILED_TIME = 10


