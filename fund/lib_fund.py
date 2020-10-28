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
from lxml import etree
import csv
import time
import functools
import inspect
import ast


# 装饰器:执行时间统计
def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(f"函数名:[{func.__name__}]执行耗时:[{t2 - t1}] seconds.")

    return wrapper


# 装饰器: delay 延迟执行
def delay(sec):
    def wrapper(func):
        @functools.wraps(func)
        def _delay_wrapper(self, *args, **kwargs):
            time.sleep(sec)
            print(f"延迟执行,函数名:[{func.__name__}],参数:[args={args}, kwargs={kwargs}]  延迟:[{sec}]s...")
            func(self, *args, **kwargs)

        return _delay_wrapper

    return wrapper


# 装饰器: retry重试函数
def retry(max_retries, count_down):
    assert max_retries and count_down, "轮询次数(count)以及轮询间隔(sec)必须大于0"

    def wrapper(func):
        @functools.wraps(func)
        def _retry_wrapper(*args, **kwargs):
            argsinps = inspect.getfullargspec(func)
            for current_retry in range(max_retries + 1):
                if 'current_retry' in argsinps.args:
                    kwargs['current_retry'] = current_retry

                try:
                    return func(*args, **kwargs)
                except Exception as err_info:
                    print(f"erro_info:[{err_info}]")
                    print(f"执行重试, 函数名:[{func.__name__}], 参数:[ kwargs={kwargs}], 当前重试次数:[{current_retry + 1}]")
                    if current_retry < max_retries + 1:
                        print(f"need wait [{count_down}] seconds...")
                        time.sleep(count_down)
                        continue
                    print(f"达到最大重试执行次数.....")
                    raise

        return _retry_wrapper

    return wrapper


class libFund(MyLogger):
    _current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    _current_day = datetime.datetime.now().strftime('%Y%m%d')

    def __init__(self, fund_code_list: list = None, level=logging.INFO):
        """
        @param fund_code_list: 手动传入列表，否则使用配置文件中的列表
        @param level:日志级别
        """
        super().__init__(__name__, level)
        self.scrpy = libScrpy(level=logging.WARNING)
        self.fund_list = []
        if fund_code_list:
            self.fund_list = fund_code_list
        else:  # 读取配置文件的基金列表
            dict = self.__json_to_dict()
            for k, v in dict.items():
                self.fund_list.append(v['code'])
        # 名称 基金净值 基金
        self.name, self.jjjz, self.gsz, self.dwjz= self.fund_current_jjjz()

    def __json_to_dict(self, json_name: str = "fund_list.json"):
        """
        将json的格式转换为字典,方便后续处理
        :param json_name: 默认json文件名
        :return:
        """
        dict = json.load(open(json_name, 'r',encoding='utf-8'))
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
        dwjz = []
        for i in range(len(list_a)):
            self.logger.info(f"request fund_code:[{list_a[i]}]")
            text = self.scrpy.single_request(list_a[i], flag=2, method=0)
            data_dict = self.__re_current_jjjz(content=text)
            name.append(data_dict['name'])
            jjjz.append(data_dict['gszzl'])
            gsz.append(data_dict['gsz'])
            dwjz.append(data_dict['dwjz'])

        # 展示基金名字+实时估算净值
        for i in range(len(name)):
            self.logger.info(f"[{name[i]}]:涨跌幅[{jjjz[i]}]")

        return name, jjjz, gsz, dwjz

    def fund_rate_estimate(self):
        """
        根据cost成本估算当前净值下的持有历史总收益率
        :return: 收益率列表
        """
        dict1 = self.__json_to_dict()

        costs = []
        for k, v in dict1.items():
            costs.append(v['cost'])

        rates = []
        for i in range(len(self.name)):
            rate = (float(self.gsz[i]) / costs[i] - 1) * 100
            rates.append(rate)
            self.logger.info(f"[{self.name[i]}]:持有收益率[{rates[i]:.2f}%]")

        return rates

    def fund_hold_amount_income(self):
        """
        估算当前净值下的持有总金额及总收益金额
        :return: 持有总金额和总收益金额的列表
        """
        dict1 = self.__json_to_dict()

        codes = []
        costs = []
        numbers = []
        for k, v in dict1.items():
            codes.append(v['code'])
            costs.append(v['cost'])
            numbers.append(v['num'])

        total_amount = []
        income_amount = []
        curr_amount = []
        for i in range(len(self.name)):
            # 持有总金额 = 份额 * 前一日净值 : 换一种方式
            pre_jjjz = float(self.dwjz[i])
            t_amount = float(pre_jjjz) * numbers[i]
            # 持有总收益 = 持有总金额 - 份额 * 成本价(cost)
            t_income = t_amount - (costs[i] * numbers[i])
            # 当日收益估算 = 当日涨跌幅 * 持有总金额
            curr_income = float(self.jjjz[i]) * t_amount / 100

            total_amount.append(t_amount)
            income_amount.append(t_income)
            curr_amount.append(curr_income)

            self.logger.info(
                f"[{self.name[i]}]:当日收益估算[{curr_amount[i]:.2f}]:持有总收益[{income_amount[i]:.2f}]:持有总金额[{total_amount[i]:.2f}]")

        return curr_amount, income_amount, total_amount

    def fund_history_jjjz(self, code: str, day: int = 3):
        """
        历史单位净值和累计净值展示
        数据来源url: 单页超过49个无效：http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=512000&per=49&page=2
        :param code:int 要查询的单个基金代码
        :param day:展示天数
        :return: 历史day天的净值 日增长率等信息等列表
        """
        assert code, "基金代码必传"
        page = day // 49 + 1  # 要请求的页数
        hisjz_list = []
        for p in range(page):
            content = self.scrpy.single_request(code=code, flag=3, day=49, page=p + 1)  # day=49固定,分页最大49
            jz_data = self.__re_history_jjjz(content)
            # self.logger.info(jz_data)
            for i in range(len(jz_data)):
                hisjz_list.append(jz_data[i])
        hisjz_list = hisjz_list[:day]

        self.logger.info(f"净值日期	单位净值	累计净值	日增长率")
        for i in range(len(hisjz_list)):
            self.logger.info(hisjz_list[i])
        # day天的总收益率
        rates_in_day = 0
        for i in range(len(hisjz_list)):
            rates_in_day += float(hisjz_list[i][3])
        # self.logger.info(f"\n该基金最近 [{day}] 天总收益率为:[ {rates_in_day:.2f} ]\n")

        return hisjz_list

    @retry(2, 5)
    # @delay(2)
    # @timer
    def fund_hold_shares(self, code: str):
        """
        单个基金持仓股票及其实时涨跌幅
        数据来源url:http://fundf10.eastmoney.com/ccmx_512000.html
        :return: 基金的前10持仓股票的基本信息列表
        """
        assert code, "基金代码必传"
        content = self.scrpy.single_request(code=code, method=1, flag=4)
        quote_info_list = self.__re_quote_hold(content)

        for i in range(len(quote_info_list)):
            self.logger.info(f"[{i+1}]:{quote_info_list[i]}")

        return quote_info_list

    def __code_to_name(self, code: str):
        """
        根绝code得到基金名称
        :param code:
        :return:
        """
        resp = self.fund_all_funds()

        re_rule = {
            1: "\"xxxxxx\",\".*?\",\"(.*?)\",",
        }
        re_res = re.findall(re_rule[1].replace('xxxxxx', code), str(resp))
        # self.logger.info(f"re_res is : {re_res[0]}")
        if re_res[0]:
            code_name = re_res[0]
        return code_name

    def fund_all_funds(self):
        """
        目前市场上所有成立的基金
        数据来源:http://fund.eastmoney.com/js/fundcode_search.js
        :return:
        """
        url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        resp = self.scrpy.request_method(url)
        return resp

    def __re_current_jjjz(self, content):
        """
        func:匹配基金实时净值估算涨跌幅
        :param content:
        :return:
        """
        re_rules = {
            'gsname': '"name":"(.*?)"',
            'dict_str': 'jsonpgz\((.*?)\);'
        }
        dict_str = re.findall(re_rules['dict_str'], str(content))
        dict_t = ast.literal_eval(dict_str[0])

        return dict_t

    def __re_history_jjjz(self, content):
        """
        func:获取基金单位净值净值和累计净值及增长率
        :param content:
        :param day: 需要获取的天数
        :return:
        """
        re_rules = {
            "1": "<tr><td>(.*?)</td><td class='tor bold'>(.*?)</td><td class='tor bold'>(.*?)</td><td class='tor bold .*?'>(.*?)%</td><td>.*?</td><td>.*?</td><td class='red unbold'></td></tr>",
            "2": "<tr>(.*?)</tr>"
        }
        resp = re.findall(re_rules["1"], str(content), re.S | re.M)
        # self.logger.info(len(resp))
        # for i in range(len(resp)):
        #     self.logger.info(resp[i])
        if resp:
            return resp

    def __re_quote_hold(self, content):
        """
        使用xpath匹配基金的股票持仓,市值,涨跌幅等信息
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        # html = etree.parse(content, etree.HTMLParser()) #文件
        xpath_rules = {
            1: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[1]/text()',  # 序号
            2: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[2]/a/text()',  # 股票代码
            3: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[3]/a/text()',  # 股票名称
            4: '//*[@id="dq600030"]/text()',  # 最新价 //*[@id="dq600030"]
            5: '//*[@id="zd600030"]/text()',  # 涨跌幅
            6: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[7]/text()',  # 持仓占比
            7: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[8]/text()',  # 持仓股数万
            8: '//*[@id="cctable"]/div[1]/div/table/tbody/tr[1]/td[9]/text()'  # 持仓市值
        }

        # @herf : 链接 text() 文本
        listA = []
        for k in range(10):
            listB = []
            for i in range(8):
                if i + 1 == 4:
                    res = html.xpath(xpath_rules[i + 1].replace('dq600030', f"dq{listB[1]}"))
                elif i + 1 == 5:
                    res = html.xpath(xpath_rules[i + 1].replace('zd600030', f"zd{listB[1]}"))
                else:
                    res = html.xpath(xpath_rules[i + 1].replace('tr[1]', f"tr[{k + 1}]"))
                listB.append(res[0])
            listA.append(listB)
        # for i in range(len(listA)):
        #     self.logger.info(f"listA[{i}] is:{listA[i]}")

        return listA

    def match_rule_bs4(self):
        """
        提取数据规则:使用bs4:Beautiful Soup
        :return:
        """
        pass

    def match_rule_xpath(self):
        """
        提取数据规则:使用xpath规则
        :return:
        """
        pass

    def csv_save(self, listA: list, title: list, csv_name: str = _current_day):
        """
        数据存储进csv文件:
        :param title:
        :param listA:
        :param csv_name:
        :return:
        """
        self.logger.info(f"csv_file:{csv_name}")
        with open(csv_name, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(title)
            for row in listA:
                writer.writerow(row)
                # writer.writerows(row)
        self.logger.info(f"save csv:[{csv_name}] finish...")

    def csv_read(self, csv_name: str):
        """
        从csv文件读取数据存储为list
        :param csv_name:
        :return:
        """
        self.logger.info(f"csv_file:{csv_name}")
        with open(csv_name, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f)
            # reader = csv.DictReader(f) # row['序号']
            for row in reader:
                self.logger.info(row) # row[0]
                # writer.writerows(row)
        self.logger.info(f"read csv:[{csv_name}] finish...")

    def db_save(self):
        """
        保存到DB数据库
        :return:
        """
        pass

    def db_read(self):
        """
        从DB读取数据
        :return:
        """
        pass

    def data_show(self, show_type: str):
        """
        数据展示 eg:第三方库
        :param show_type: to do
        :return:
        """
        pass


if __name__ == "__main__":
    fund_code_list = ['512000', '270002']  # ,'000478','110035','001210','008488','001938','002621']
    ff = libFund(level=logging.INFO)
    # 获取基金列表的实时涨跌幅
    # ff.fund_current_jjjz()
    # 获取基金列表的持有收益率
    ff.fund_rate_estimate()
    # 获取基金列表的持有总金额和持有收益金额,实时估算收益
    ff.fund_hold_amount_income()
    # 获取单个基金的历史几天的 单位净值 历史净值 日收益率
    ff.fund_history_jjjz('512000', 1)
    # 获取单个基金的股票持仓情况及股票实时的涨跌幅
    ff.fund_hold_shares('270002')
