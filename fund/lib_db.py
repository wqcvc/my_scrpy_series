# -*- coding: utf-8 -*-
"""
 @Topic:db相关操作
 @Date: 2020-9-15
 @Author: terry.wang
"""

import pymysql
pymysql.install_as_MySQLdb()
# wait to learn
from urllib.parse import quote_plus
from sqlalchemy import event, exc, select, orm, create_engine
from jsonrpc_requests.jsonrpc import Method
from werkzeug.local import LocalStack


class libDB():
    def __init__(self):
        self.db = pymysql.Connect(host='127.0.0.1', user="root", password="km9m77wq123", port=3306, database="scrpy")
        self.cursor = self.db.cursor()
        # assert sql_method in ['select', 'update', 'insert', 'delete'], '不支持的强化版SQL方法: {}'.format(method_name)

    def create_table(self, sql: str):
        pass

    def query(self, sql: str):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            # results = self.cursor.fetchone()
            print(f"results is : {results}")
        except:
            print(f"Error:unable to fetch data")


from sqlalchemy import create_engine


class Engine(object):

    def __init__(self, mysql_options, session_options, engine_options, **_mysql_options):
        self.engine = None
        self._session_options = session_options or {}
        self._engine_options = self.get_engine_options(engine_options)
        self.my_options = mysql_options or _mysql_options
        self._sa_url = self.get_url(self.my_options)

    def get_url(self, my_options):
        username = my_options.get('username', 'root')
        password = my_options.get('password', 'km9m77wq123')
        host = my_options.get('host') or my_options.get('ip')
        assert host, 'host/ip 必填'
        port = my_options.get('port', 3306)
        db = my_options.get('db') or my_options.get('schema') or ''
        return f'mysql+pymysql://{username}:{quote_plus(password)}@{host}:{port}/{db}?charset=utf8'

    def get_engine_options(self, engine_options):
        engine_options = engine_options or {}
        engine_options.setdefault('pool_size', 10)
        engine_options.setdefault('pool_recycle', 60 * 2)
        engine_options.setdefault('pool_pre_ping', True)
        engine_options.setdefault('echo', True)
        return engine_options

class AA(object):
    def exec(self):
        print(f"AA exec!")

class BB(object):
    def exec(self):
        pass
    def xxx(self):
        return self.exec()

class CC(AA,BB):
    def exec(self):
        res=super().exec()
        return res





# if __name__ == "__main__":
#     test_db = libDB()
#     sql_1 = "select * from user1;"
#     test_db.query(sql_1)
#
#     c1=CC()
#     res=c1.exec()


"""
sqlalchemy入门
Engine: 连接
Session: 连接池
Model: 表
Colnum: 列 
Query: 若干行
"""
from sqlalchemy import create_engine

engine = create_engine("mysql://root:km9m77wq123@127.0.0.1:3306/scrpy?charset=utf8",
                       echo=True,  # echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
                       pool_size=10,  # pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
                       pool_recycle=60*2,  # pool_recycle: 设置时间以限制数据库多久没连接自动断开
                       pool_pre_ping=True
                       )






