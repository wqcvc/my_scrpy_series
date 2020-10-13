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
from lib_logger import MyLogger
import datetime
import re
import requests
import time
import logging


class libFund(MyLogger):
    _current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    def __init__(self, fund_code_list: list = None,level=logging.INFO):
        super().__init__(__name__,level)
        self.res = libScrpy(level)
        if fund_code_list:
            self.fund_list = fund_code_list
        else:#读取配置文件 基金列表
            self.fund_list = 0

    def current_jjjz(self, list_a: list = None):
        """
        基金实时涨跌幅 数据统一获取入口
        :return:
        """
        if not list_a:
            list_a = self.fund_list
        jjjz = []
        name = []
        for i in range(len(list_a)):
            self.logger.info(f"request fund_code:[{list_a[i]}]")
            text = self.res.single_request(list_a[i], flag=2,method=0)
            name_tmp,jjjz_tmp=self.re_current_jjjz(content=text)
            jjjz.append(jjjz_tmp)
            name.append(name_tmp)

        #展示基金名字+实时估算净值
        for i in range(len(name)):
            self.logger.info(f"[{name[i]}:{jjjz[i]}]")

    def fund_income_estimate(self,):
        """
        根据基金持有份额 估算当前涨跌幅下的当日收益
        :return:
        """
        pass

    def fund_rate_estimate(self):
        """
        根据cost成本估算当前净值下的持有历史总收益率
        :return:
        """
        pass

    def fund_history_jjjz(self, day: int = 3):
        """
        历史净值展示
        :param day:天数
        :return:
        """
        pass


    def re_current_jjjz(self, content):
        """
        func:匹配基金实时净值估算涨跌幅
        :param content:
        :return:
        """
        re_rules={
                'gz_gsz':'<span class="ui-font-large  ui-num" id="gz_gsz">(.*?)</span>',
                'name':'<div class="fundDetail-tit"><div style="float: left">(.*?)<span>',
                'gsname':'"name":"(.*?)"',
                'gszzl':'"gszzl":"(.*?)"'
                  }
        # res1=re.findall(re_rules['gz_gsz'],str(content))
        # res2=re.findall(re_rules['name'],str(content))
        name=re.findall(re_rules['gsname'],str(content))
        gszzl=re.findall(re_rules['gszzl'],str(content))

        return name[0],gszzl[0]


    def match_rule_re(self, content):
        """
        func:正则匹配获取基金实时净值和名字
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

    def data_storage(self,method:int = 0):
        """
        数据存储:
        :param method:0-mysql 1-sqlalchemy
        :return:
        """
        pass

    def data_show(self, type: str):
        """
        数据展示 eg:第三方库
        :return:
        """
        pass


if __name__ == "__main__":
    fund_code_list = ['512000','270002'] #,'000478','110035','001210','008488','001938','002621']
    ff = libFund(fund_code_list,level=logging.INFO)
    ff.current_jjjz()
