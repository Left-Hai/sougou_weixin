# -*- coding: utf-8 -*-
# author: Right.Hai
# time: 2019/04/11
# email: 1955507077@qq.com
# for: MySQL

from pymysql import connect, MySQLError
from config import *


class Mysql():
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT,
                 database=MYSQL_DATABASE):
        try:
            self.db = connect(host, username, password, database, charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except MySQLError as e:
            print(e.args)

    def insert(self, table, data={}):
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) value (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except MySQLError as e:
            print(e.args)
            self.db.rollback()


if __name__ == '__main__':
    db = Mysql()
    data = {
        'title': "test",
        'content': 'content',
        'date': '2018-04-09',
        'wechat': '中华微信',
        'nickname': '1xx233'
    }
    db.insert('articles', data)


