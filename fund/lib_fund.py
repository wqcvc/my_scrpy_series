# -*- coding: utf-8 -*-
"""
 @Topic:fund相关操作和数据
    eg. 1.展示单只实时
        2.展示历史3，7，15天数据
        3.展示过去5天总收益率
 @Date: 2020-9-15
 @Author: terry.wang
"""
from lib_scrpy import libScrpy
import datetime
import io
import os
import logging
import traceback


class libFund():
    _current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    def __init__(self , fund_code_list : list):
        self.logger=Logger()
        self.logger.setLevel(logging.INFO)
        # self.logger.format()
        self.logger.add_stream_handler()

        self.res = libScrpy()
        self.fund_list = fund_code_list
        self.logger.info("3333")
        # print(f"{self.logger.add_stream_handler()}")
        # logger.info()


    def all_get(self):
        """
        请求入口
        :return:
        """
        for i in range(len(self.fund_list)):
            text = self.res.single_request(self.fund_list[i],method=0)
            self.logger.info(f"currnet fund_code:{self.fund_list[i]}")
            self.match_rule_re(content=text)


    def match_rule_re(self, content):
        """
        提取数据规则:使用re
        :param content:
        :return:
        """

        pass

    def match_rule_bs4(self, day: int):
        """
        提取数据规则:使用bs4:Beautiful Soup
        :param day:
        :return:
        """
        pass

    def match_rule_xpath(self, day: int):
        """
        提取数据规则:使用xpath规则
        :param day:
        :return:
        """
        pass

    def data_storage(self):
        """
        数据存储:
        :return:
        """
        pass

    def data_show(self, type: str):
        """
        数据展示 eg:第三方库
        :return:
        """
        pass

if __name__== "__main__":
    fund_code_list=['512000','163406']
    ff=libFund(fund_code_list)
    ff.all_get()
