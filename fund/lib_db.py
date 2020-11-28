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


# from jsonrpc_requests.jsonrpc import Method
# from werkzeug.local import LocalStack


class libDB():
    def __init__(self, **mysql_options):
        host = mysql_options.get('host', '127.0.0.1')
        user = mysql_options.get('user', 'root')
        password = mysql_options.get('password', 'km9m77wq123')
        port = mysql_options.get('port', '3306')
        database = mysql_options.get('db', 'fund')
        self.conn = pymysql.Connect(host=host, user=user, password=password, port=port, database=database,
                                    charset='utf8')
        # assert sql_method in ['select', 'update', 'insert', 'delete'], '不支持的强化版SQL方法: {}'.format(method_name)

    def execute(self, sql: str):
        """
        操作表: create drop modify, insert update delete
        @param sql:
        @return:
        """
        assert sql, "创建表传入的 sql 不能为空"
        try:
            cursor = self.conn.cursor()
            # 执行SQL语句
            res_e = cursor.execute(sql)
            # 提交事务
            print(f"res is : [{res_e}]")
            self.conn.commit()
            cursor.close()
        except Exception as e:
            # 有异常，回滚事务
            print(f"exception info:[{e}]")
            self.conn.rollback()

    def query(self, sql: str, **fetch_method):
        """
        操作：查询表
        @param sql:
        @param fetch_method: one=one all=all num=3
        @return:
        """
        assert sql, "创建表传入的 sql 不能为空"
        try:
            cursor = self.conn.cursor()
            # 执行SQL语句
            res_c = cursor.execute(sql)
            # 提交事务
            self.conn.commit()
            if fetch_method.get('one'):
                res_q = cursor.fetchone()
            elif fetch_method.get('all'):
                res_q = cursor.fetchall()
            elif fetch_method.get('num'):
                res_q = cursor.fetchmany(fetch_method.get('num'))
            print(res_c)
            print(res_q)
            cursor.close()
        except Exception as e:
            # 有异常，回滚事务
            print(f"exception info:[{e}]")
            self.conn.rollback()

    def __del__(self):
        print("in __del__() func")
        self.conn.close()


class AA(object):
    def exec(self):
        print(f"AA exec!")


class BB(object):
    def exec(self):
        pass

    def xxx(self):
        return self.exec()


class CC(AA, BB):
    def exec(self):
        res1 = super().exec()
        return res1


# if __name__ == "__main__":
#     # pymysql的所有操作
#     test_db = libDB(host='127.0.0.1', port=3306)
#     sql_create = """
#     CREATE TABLE fund.student1(
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '学号',
#     name VARCHAR(200) COMMENT '姓名',
#     age    int COMMENT '年龄'
#     ) COMMENT='学生信息';
#     """
#     sql_modify = "alter table fund.student1 modify name VARCHAR(215) COMMENT '姓名';"
#     sql_drop = "drop table fund.student1;"
#     # test_db.execute(sql_create)
#     # test_db.execute(sql_modify)
#     # test_db.execute(sql_drop)
#
#     sql_insert = "INSERT INTO fund.student1(name, age) VALUES ('wq', 28);"
#     sql_update = " UPDATE fund.student1 SET age='22' WHERE name='wq';"
#     sql_query = "select * from fund.student1;"
#     sql_delete = "DELETE FROM fund.student1 WHERE name='wq';"
#     # test_db.execute(sql_insert)
#     # test_db.execute(sql_update)
#     # test_db.query(sql_query, one=True)
#     # test_db.execute(sql_delete)
#
#     # 类高级用法
#     c1 = CC()
#     res1 = c1.exec()


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


"""
sqlalchemy入门
Engine: 连接
Session: 连接池
Model: 表
Colnum: 列
Query: 若干行
"""
engine = create_engine("mysql://root:km9m77wq123@127.0.0.1:3306/fund?charset=utf8",
                       echo=True,  # echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
                       pool_size=10,  # pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
                       pool_recycle=60 * 2,  # pool_recycle: 设置时间以限制数据库多久没连接自动断开
                       pool_pre_ping=True
                       )
