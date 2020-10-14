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
import logging
import json


class libFund(MyLogger):
    _current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    def __init__(self, fund_code_list: list = None,level=logging.INFO):
        """
        @param fund_code_list: 手动传入列表，否则使用配置文件中的列表
        @param level:日志级别
        """
        super().__init__(__name__,level)
        self.res = libScrpy(level=logging.WARNING)
        self.fund_list=[]
        if fund_code_list:
            self.fund_list = fund_code_list
        else:  # 读取配置文件的基金列表
            dict=self.__json_to_dict()
            for k,v in dict.items():
                self.fund_list.append(v['code'])
        self.name, self.jjjz, self.gsz= self.fund_current_jjjz()


    def __json_to_dict(self,json_name:str ="fund_list.json"):
        """
        将json的格式转换为字典,方便后续处理
        :param json_name: 默认json文件名
        :return:
        """
        dict=json.load(open(json_name,'r'))
        if dict:
            return dict
        else:
            self.logger.info("json to dict failed.")


    def fund_current_jjjz(self, list_a: list = None):
        """
        基金实时涨跌幅 数据统一获取入口
        @param list_a: 基金代码列表
        @return:
        """
        if not list_a:
            list_a = self.fund_list
        jjjz = []
        name = []
        gsz = []
        for i in range(len(list_a)):
            self.logger.info(f"request fund_code:[{list_a[i]}]")
            text = self.res.single_request(list_a[i], flag=2,method=0)
            list_b=self.re_current_jjjz(content=text)
            name.append(list_b[0])
            jjjz.append(list_b[1])
            gsz.append(list_b[2])

        #展示基金名字+实时估算净值
        for i in range(len(name)):
            self.logger.info(f"[{name[i]}]:涨跌幅[{jjjz[i]}]")

        return name,jjjz,gsz

    def fund_income_estimate(self):
        """
        根据基金持有份额num 估算当前涨跌幅下的当日收益
        :return:
        """
        dict1 = self.__json_to_dict()

        numbers = []
        for k, v in dict1.items():
            numbers.append(v['num'])

        incomes = []
        for i in range(len(self.name)):
            incomes.append(float(self.jjjz[i]) * numbers[i])
            self.logger.info(f"[{self.name[i]}]:涨跌幅[{self.jjjz[i]}]:估算收益[{incomes[i]:.2f}]")

        return incomes


    def fund_rate_estimate(self):
        """
        根据cost成本估算当前净值下的持有历史总收益率
        :return:
        """
        dict1 = self.__json_to_dict()

        costs = []
        for k, v in dict1.items():
            costs.append(v['cost'])

        rates=[]
        for i in range(len(self.name)):
            rate=(float(self.gsz[i])/costs[i]-1)*100
            rates.append(rate)
            self.logger.info(f"[{self.name[i]}]:持有收益率[{rates[i]:.2f}%]")

        return rates


    def fund_hold_amount_income(self):
        """
        估算当前净值下的持有总金额及总收益金额
        :return:
        """
        dict1 = self.__json_to_dict()

        costs = []
        numbers = []
        for k, v in dict1.items():
            costs.append(v['cost'])
            numbers.append(v['num'])

        total_amount = []
        income_amount = []
        for i in range(len(self.name)):
            amount=(float(self.gsz[i]))*numbers[i]
            income=(float(self.gsz[i])/costs[i]-1)*numbers[i]
            total_amount.append(amount)
            income_amount.append(income)
            self.logger.info(f"[{self.name[i]}]:持有收益[{income_amount[i]:.2f}]:持有总金额[{total_amount[i]:.2f}]")

        return total_amount,income_amount


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
                'gszzl':'"gszzl":"(.*?)"',
                'gsz':'"gsz":"(.*?)"'
                  }
        # res1=re.findall(re_rules['gz_gsz'],str(content))
        # res2=re.findall(re_rules['name'],str(content))
        name=re.findall(re_rules['gsname'],str(content))
        gszzl=re.findall(re_rules['gszzl'],str(content))
        gsz=re.findall(re_rules['gsz'],str(content))

        list_t=[]
        list_t.append(name[0])
        list_t.append(gszzl[0])
        list_t.append(gsz[0])
        return list_t


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
    # ff.fund_current_jjjz()
    ff.fund_income_estimate()
    ff.fund_rate_estimate()
    ff.fund_hold_amount_income()
