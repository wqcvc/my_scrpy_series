# -*- coding: utf-8 -*-
"""
 @Topic:fund相关操作和数据
    eg. 1.展示单只实时
        2.展示历史3，7，15天数据
        3.展示过去5天总收益率
 @Date: 2020-9-15
 @Author: terry.wang
"""
from my_scrpy_series.fund import *
import re
import requests
import datetime
import logging


class libFund():
    _current_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    def __init__(self,fund_code_list:list):
        self.res=libScrpy().apply()
        self.res.apply(fund_code_list[0])


    def total_rate_show(self):
        pass

    def rate_list_show(self,day:int):

    def count_rate(self,day:int):
        pass

    def showtime(self,type:str):
        """
        数据展示方式
        :return:
        """



