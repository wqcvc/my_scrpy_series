# -*- coding: utf-8 -*-
"""
 @Topic:db相关操作
 @Date: 2020-9-15
 @Author: terry.wang
"""

import pymysql


class libDB():
    def __init__(self):
        self.db = pymysql.Connect(host='127.0.0.1', user="root", password="km9m77wq123", port=3306, database="scrpy")
        self.cursor = self.db.cursor()

    def create_table(self,sql:str):


    def query(self, sql: str):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            # results = self.cursor.fetchone()
            print(f"results is : {results}")
        except:
            print(f"Error:unable to fetch data")


if __name__ == "__main__":
    test_db = libDB()
    sql_1 = "select * from user1;"
    test_db.query(sql_1)
