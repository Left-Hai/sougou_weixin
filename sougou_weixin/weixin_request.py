# -*- coding: utf-8 -*-
# author: Right.Hai
# time: 2019/00/00
# email: 1955507077@qq.com
# for:

from requests import Request

TIMEOUT = 10


class WeixinRequest(Request):
    """
    继承Request并实现添加三个属性：need_proxy,fail_time,callback用作请求队列
    """

    def __init__(self, url, callback, headers=None, method='GET', need_proxy=False, fail_time=0, timeout=TIMEOUT,
                 referer=None, allow_redirects=False):
        Request.__init__(self, method, url, headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout
        self.Referer = referer
        self.allow_redirects = allow_redirects
