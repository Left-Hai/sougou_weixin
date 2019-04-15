# -*- coding: utf-8 -*-
# author: Right.Hai
# time: 2019/04/11
# email: 1955507077@qq.com
# for: 构造请求队列，实现请求的存取

from pickle import dumps, loads
from weixin_request import WeixinRequest
from redis import StrictRedis
from config import *


class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)

    def add(self, request):
        """
        向数据库加入序列化后的request
        :param request: 请求对象
        :return: 添加结果
        """
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        """
        取出一条数据，并反序列化返回
        :return: Request or False
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        """
        判断是否为空
        :return:
        """
        return self.db.llen(REDIS_KEY) == 0










