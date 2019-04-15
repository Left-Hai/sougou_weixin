# -*- coding: utf-8 -*-
# author: Right.Hai
# time: 2019/00/00
# email: 1955507077@qq.com
# for:
import re
import time
import requests
from requests import Session
from redis_queue import RedisQueue
from api_mysql import Mysql
from weixin_request import WeixinRequest
from urllib.parse import urlencode
from requests.exceptions import ReadTimeout, ConnectionError
from pyquery import PyQuery as pq
from config import *


class Spider(object):
    def __init__(self):
        self.base_url = "https://weixin.sogou.com/weixin"
        self.keyword = KEY
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': COOKIES,
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.86 Safari/537.36',
        }
        self.session = Session()
        self.queue = RedisQueue()
        self.mysql = Mysql()

    def start(self):
        # 这里更新会后面请求头请求会302， 在wei_request里更新请求头
        # self.session.headers.update(self.headers)
        param = {
            'query': self.keyword,
            'type': 2
        }
        start_url = self.base_url + '?' + urlencode(param)
        weixin_request = WeixinRequest(url=start_url, headers=self.headers, callback=self.parse_index, need_proxy=True)
        self.queue.add(weixin_request)

    def schedule(self):
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            print("SChedule", weixin_request.url)
            response = self.request(weixin_request)
            if response and response.status_code in VALID_STATUS:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New Request', result)
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('articles', result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def request(self, request):
        time.sleep(1)
        try:
            if request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' + str(proxy),
                        'https': 'https://' + str(proxy)
                    }
                    return self.session.send(request.prepare(), timeout=request.timeout,
                                             allow_redirects=request.allow_redirects, proxies=proxies)
            return self.session.send(request.prepare(), timeout=request.timeout,
                                     allow_redirects=request.allow_redirects)
        except (ConnectionError, ReadTimeout) as e:
            print(e)
            return False

    def get_proxy(self):
        for i in range(5):
            response = requests.get(PROXY_URL)
            if response.status_code == 200:
                return response.text
        return False

    def parse_index(self, response):
        doc = pq(response.text)
        items = doc('h3 a').items()
        for item in items:
            url = item.attr('data-share')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail, allow_redirects=True)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)
            page = int(re.findall('page=(\d+)', url)[0]) - 1
            referer = re.sub('page=\d+', str('page=' + str(page)), url)
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True, referer=referer,
                                           headers=self.headers)
            yield weixin_request

    def parse_detail(self, response):
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text().strip(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#publish_time').text(),
            'nickname': doc('.profile_nickname').text(),
            'wechat': doc('div.profile_inner > p:nth-child(3) > span').text()
        }
        yield data

    def error(self, request):
        request.fail_time += 1
        print('Request Failed', request.fail_time, 'times', request.url)
        if request.fail_time < MAX_FAILED_TIME:
            self.queue.add(request)

    def run(self):
        self.start()
        self.schedule()


if __name__ == '__main__':
    a = Spider()
    a.run()



