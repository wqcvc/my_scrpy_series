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


class libFund(MyLogger):
    _current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    def __init__(self, fund_code_list: list):
        super().__init__(__name__)
        self.res = libScrpy()
        self.fund_list = fund_code_list

    def all_get(self):
        """
        请求入口
        :return:
        """
        jjjz=[]
        name=[]
        #拿基金的估算净值
        resxxx=requests.get(url='http://fundgz.1234567.com.cn/js/002621.js')
        # resxxx=requests.get(url='http://fundgz.1234567.com.cn/js/270002.js')
        resxxx.encoding="utf-8"
        tmp1=re.findall('"gszzl":"(.*?)"',str(resxxx.text))
        print(tmp1)
        for i in range(len(self.fund_list)):
            self.logger.info(f"request fund_code:[{self.fund_list[i]}]")
            text = self.res.single_request(self.fund_list[i], method=0)
            jjjz_tmp,name_tmp=self.match_rule_re(content=text)
            jjjz.append(jjjz_tmp)
            name.append(name_tmp)

        #展示基金名字+实时估算净值
        for i in range(len(name)):
            self.logger.info(f"[{name[i]}:{jjjz[i]}]")

    def match_rule_re(self, content):
        """
        提取数据规则:使用re
        :param content:
        :return:
        """
        # <span class="ui-font-large  ui-num" id="gz_gsz">--</span>  .*? 非贪婪模式
        re_rules={
                'gz_gsz':'<span class="ui-font-large  ui-num" id="gz_gsz">(.*?)</span>',
                'name':'<div class="fundDetail-tit"><div style="float: left">(.*?)<span>'
                  }
        # self.logger.info(content)
        res1=re.findall(re_rules['gz_gsz'],str(content))
        res2=re.findall(re_rules['name'],str(content))
        # self.logger.info(f"re_match res is [{res1[0],res2[0]}]")

        return res1[0],res2[0]

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


if __name__ == "__main__":
    fund_code_list = ['512000','270002'] #,'000478','110035','001210','008488','001938','002621']
    ff = libFund(fund_code_list)
    ff.all_get()
