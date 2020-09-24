# -*- coding: utf-8 -*-
"""
 @Topic:爬取的相关:
        1.数据获取
        2.数据处理
        3.数据存储...
 @Date: 2020-9-15
 @Author: terry.wang
"""
import requests
import os
import execjs
import datetime
import re
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger()


class libScrpy():
    _data_source_url='http://fund.eastmoney.com/xxx.html'
    # f"http://fund.eastmoney.com/{code}.html"
    # http: // fundf10.eastmoney.com / jjjz_270002.html
    _current_time=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


    def __init__(self):
        pass

    def apply(self,url):
        """
        爬
        :param url:抓qu地址
        :return:
        """

    def re_match_rule(self):
        """

        :return:
        """

    def store_data(self):

