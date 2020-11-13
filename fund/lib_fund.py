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
import asyncio
import pandas as pd


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
    # 使用东财数据
    _data_source_url = 'http://fund.eastmoney.com/xxx.html'
    _current_jjjz_url = 'http://fundgz.1234567.com.cn/js/xxx.js'
    _history_jjjz_url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=xxx&per=ddd&page=ppp'
    _quote_hold_url = 'http://fundf10.eastmoney.com/ccmx_xxx.html'

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
        # 基金名称 基金涨跌幅 估算净值 前日净值
        list_tmp = self.fund_current_jjjz()
        self.name, self.gszzl, self.gsz, self.dwjz = [],[],[],[]
        for i in range(len(self.fund_list)):
            self.name.append(list_tmp[i][0])
            self.gszzl.append(list_tmp[i][1])
            self.gsz.append(list_tmp[i][2])
            self.dwjz.append(list_tmp[i][3])

    def fund_current_jjjz(self, list_a: list = None):
        """
        基金实时涨跌幅 数据统一获取入口
        @param list_a: 基金代码列表
        @return:
        """
        if not list_a:
            list_a = self.fund_list

        total_data = []
        for i in range(len(list_a)):
            self.logger.info(f"request fund_code:[{list_a[i]}]")
            text = self.__fund_request_by_code(list_a[i], flag=2, method=0)
            data_dict = self.__re_current_jjjz(content=text)
            total_data.append([data_dict['name'], data_dict['gszzl'], data_dict['gsz'], data_dict['dwjz']])

        return total_data

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

        return rates

    @property
    def fund_hold_info(self):
        """
        估算当前净值下的持有总金额及总收益金额 + 持有收益率 + 涨跌幅
        :return: 持有总金额和总收益金额的列表 + 持有收益率 + 涨跌幅
        """
        dict1 = self.__json_to_dict()

        codes, costs, numbers= [],[],[]
        for k, v in dict1.items():
            codes.append(v['code'])
            costs.append(v['cost'])
            numbers.append(v['num'])

        rates = self.fund_rate_estimate()
        total_amount, income_amount, curr_amount = [], [], []
        xyz1, xyz2, xyz3 = 0, 0, 0
        for i in range(len(self.name)):
            # 持有总金额 = 份额 * 前一日净值 : 换一种方式
            pre_jjjz = float(self.dwjz[i])
            t_amount = float(pre_jjjz) * numbers[i]
            # 持有总收益 = 持有总金额 - 份额 * 成本价(cost)
            t_income = t_amount - (costs[i] * numbers[i])
            # 当日收益估算 = 当日涨跌幅 * 持有总金额
            curr_income = float(self.gszzl[i]) * t_amount / 100

            curr_amount.append(curr_income)
            income_amount.append(t_income)
            total_amount.append(t_amount)

            self.logger.info(
                f"[{self.name[i]}]: 实时涨跌幅[{self.gszzl[i]}%] 当日收益估算[{curr_amount[i]:.2f}] 持有收益率[{rates[i]:.2f}%] 持有总收益[{income_amount[i]:.2f}] "
                f"持有总金额[{total_amount[i]:.2f}]")

            xyz1 += curr_income
            xyz2 += t_income
            xyz3 += t_amount

        self.logger.info(f"当日总收益:[{xyz1}] 持有总收益:[{xyz2}] 持有总额:[{xyz3}] ")

        all_info = []
        for i in range(len(self.name)):
            all_info.append(
                [self.name[i], codes[i], self.gszzl[i], curr_amount[i], rates[i], income_amount[i], total_amount[i]])
        all_info.append([f"当日总收益:[{xyz1}]", f"持有总收益:[{xyz2}]", f"持有总额:[{xyz3}]"])

        return all_info

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
            content = self.__fund_request_by_code(code=code, flag=3, day=49, page=p + 1)  # day=49固定,分页最大49
            jz_data = self.__re_history_jjjz(content)
            for i in range(len(jz_data)):
                hisjz_list.append(jz_data[i])
        hisjz_list = hisjz_list[:day]

        # day天的总收益率
        rates_in_day = 0
        for i in range(len(hisjz_list)):
            rates_in_day += float(hisjz_list[i][3])

        # 转换为 Dataframe 格式
        df_hisjz = pd.DataFrame(hisjz_list,columns=['净值日期', '单位净值', '累计净值', '日增长率'])
        # df_hisjz.to_excel('xxx1.xlsx',index=False)

        self.logger.info(df_hisjz)
        return df_hisjz

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
        content = self.__fund_request_by_code(code=code, method=1, flag=4)
        quote_info_list = self.__re_quote_hold(content)

        for i in range(len(quote_info_list)):
            self.logger.info(f"[{i + 1}]:{quote_info_list[i]}")

        return quote_info_list

    def fund_his_rates(self, code: str):
        """

        :param code: 基金代码
        :param  : 涨幅: 1-阶段涨幅 2-季度涨幅 3-年度涨幅 4-持有人结构
        :return:
        """
        # 阶段涨幅   http://fundf10.eastmoney.com/jdzf_270002.html
        # 季度年涨幅  http://fundf10.eastmoney.com/jndzf_270002.html
        # 持有人结构  http://fundf10.eastmoney.com/cyrjg_270002.html

        #阶段涨幅
        content1 = self.__fund_request_by_code(code=code, flag=5, method=1)
        res1,res1_t = self.__re_fund_jdzf(content=content1)
        #季度/年涨幅
        content2 = self.__fund_request_by_code(code=code, flag=6, method=1)
        res2,res2_t = self.__re_fund_jndzf(content=content2)
        # 持有人结构
        content3 = self.__fund_request_by_code(code=code, flag=7, method=1)
        res3,res3_t = self.__re_fund_cyrjg(content=content3)

        res_f_t = res1_t + res2_t + res3_t
        res_f = [res1 + res2 + res3]
        df_f = pd.DataFrame(res_f,columns=res_f_t)
        self.logger.info(df_f)
        # df_f.to_excel("xs.xlsx")
        return df_f

    def fund_basic_info(self, code: str):
        """
        基金规模数据+基金经理信息
        :param code:
        :param : 1.规模+规模增长数据 2.基金经理个人,管理规模,业绩等信息
        :return:
        """
        # 规模变动  http://fundf10.eastmoney.com/gmbd_270002.html
        content1 = self.__fund_request_by_code(code=code, flag=8, method=1)
        res1,res1_t = self.__re_fund_gmbd(content=content1)

        # 基金经理  http://fundf10.eastmoney.com/jjjl_270002.html
        content2 = self.__fund_request_by_code(code=code, flag=9, method=1)
        res2,res2_t = self.__re_fund_jjjl(content=content2)

        res_f= [res1 + res2]
        res_f_t = res1_t + res2_t
        df_f = pd.DataFrame(res_f,columns=res_f_t)
        self.logger.info(df_f)

        return df_f

    def fund_special_info(self, code: str):
        """
        基金特色数据
        :param code:
        :param : 1.近1年夏普比率  2.近1年波动率 3.近1年最大回撤 4.近1年最大回撤率
        :return:
        """
        # 特殊数据 http://fundf10.eastmoney.com/tsdata_270002.html
        content1 = self.__fund_request_by_code(code=code, flag=10, method=1)
        res1,res1_t = self.__re_fund_tsdata(content=content1)

        res_f = [res1]
        df_f = pd.DataFrame(res_f, columns=res1_t)
        self.logger.info(df_f)

        return df_f

    def funds_all_list(self,to_file):
        """
        只取市场上所有开放基金的列表,存入xlsx
        :param to_file:是否写入xlsx文件
        :return:
        """
        resp = self.__funds_list()

        re_rule = {
            2: "\"(.*?)\",\".*?\",\"(.*?)\",\"(.*?)\",\".*?\""
        }

        re_res2 = re.findall(re_rule[2],str(resp))
        lpd = pd.DataFrame(re_res2,columns=['code','name','type'])
        if to_file == 1:
            lpd.to_excel('all_funds.xlsx',index=False)
            self.logger.info(f"all_funds write to xlsx file finish.")
        else:
            pass

        return lpd

    def code_to_name(self, code: str):
        """
        根绝code得到基金名称
        :param code:
        :return:
        """
        resp = self.__funds_list()

        re_rule = {
            1: "\"xxxxxx\",\".*?\",\"(.*?)\","
        }
        re_res= re.findall(re_rule[1].replace('xxxxxx', code), str(resp))
        if re_res[0]:
            code_name = re_res[0]

        return code_name

    def __re_fund_jdzf(self, content):
        """
        使用xpath匹配基金的阶段涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="jdzftable"]/div/ul[2]/li[2]/text()',   # 今年来  近1周  近1，3，6个月  近1，2，3，5年 成立以来 ul+
            2: '//*[@id="jdzftable"]/div/ul[2]/li[1]/text()'   # 标题 ul+
        }

        listA = []
        list_t = []
        for i in range(10):
            res = html.xpath(xpath_rules[1].replace('ul[2]',f"ul[{i+2}]"))
            res2 = html.xpath(xpath_rules[2].replace('ul[2]',f"ul[{i+2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            list_t.append(res2[0])
        return listA,list_t

    def __re_fund_jndzf(self, content):
        """
        使用xpath匹配基金的季度/年涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="quarterzftable"]/table/tbody/tr[1]/td[2]/text()',   # 季度涨幅 td+
            2: '//*[@id="yearzftable"]/table/tbody/tr[1]/td[2]/text()',   # 年度涨幅 td+
            3: '//*[@id="quarterzftable"]/table/thead/tr/th[2]/text()',   # 季度标题 th+
            4: '//*[@id="yearzftable"]/table/thead/tr/th[2]/text()'   # 年度标题 th+
        }

        # 最近8个季度的涨幅
        listA = []
        list_t = []
        for i in range(8):
            res = html.xpath(xpath_rules[1].replace('td[2]',f"td[{i+2}]"))
            res2 = html.xpath(xpath_rules[3].replace('th[2]',f"th[{i+2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            list_t.append(res2[0])

        # 最近8年的业绩
        for i in range(8):
            res = html.xpath(xpath_rules[2].replace('td[2]',f"td[{i+2}]"))
            res2 = html.xpath(xpath_rules[4].replace('th[2]',f"th[{i+2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            list_t.append(res2[0])

        return listA,list_t

    def __re_fund_cyrjg(self, content):
        """
        使用xpath匹配基金的持有人结构
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="cyrjgtable"]/table/tbody/tr[1]/td[1]/text()',   # 只要最近更新的一期结构中 各占比例即可。 日期 机构 个人 内部 总份额 td+
            2: '//*[@id="cyrjgtable"]/table/thead/tr/th[1]/text()'   # 标题 th+

        }

        listA = []
        list_t = []
        for i in range(5):
            res = html.xpath(xpath_rules[1].replace('td[1]',f"td[{i+1}]"))
            res2 = html.xpath(xpath_rules[2].replace('th[1]',f"th[{i+1}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            list_t.append(res2[0])
        return listA,list_t

    def __re_fund_gmbd(self, content):
        """
        使用xpath匹配基金的规模变动
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="gmbdtable"]/table/tbody/tr[1]/td[5]/text()',   # 最近8期的规模变动 tr+ //*[@id="gmbdtable"]/table/tbody/tr[2]/td[5]
            2: '//*[@id="gmbdtable"]/table/tbody/tr[1]/td[1]/text()'   # 标题 tr+   //*[@id="gmbdtable"]/table/tbody/tr[2]/td[1]

        }

        listA = []
        list_t = []
        # 最近8个季度的规模变动信息
        for i in range(8):
            res = html.xpath(xpath_rules[1].replace('tr[1]',f"tr[{i+1}]"))
            res2 = html.xpath(xpath_rules[2].replace('tr[1]',f"tr[{i+1}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])
        return listA,list_t

    def __re_fund_jjjl(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[1]/text()',   # 起始期
            2: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[2]/text()',  # 截止期
            3: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[3]/a/text()',  # 基金经理
            4: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/text()',  # 任职时间
            5: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[5]/text()',  # 任职回报
            6: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/thead/tr/th[1]/text()'   # title合集 th+
        }

        listA = []
        list_t = []
        # 最近1个经理任期业绩 5项数据
        for i in range(5):
            res = html.xpath(xpath_rules[i+1])
            res_t = html.xpath(xpath_rules[6].replace('th[1]', f"th[{i+1}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
            list_t.append(res_t[0])

        return listA,list_t

    def __re_fund_tsdata(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[2]/td[2]/text()',   # 近1年标注差
            2: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[3]/td[2]/text()',  # 近1年夏普率
            3: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[2]/td[1]/text()',  # 标准差 title td
            4: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[3]/td[1]/text()',  # 夏普率
        }

        listA = []
        list_t = []
        # 最近1个经理任期业绩
        for i in range(2):
            res = html.xpath(xpath_rules[i+1])
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
        for i in range(2):
            res_t = html.xpath(xpath_rules[i+3])
            if not res_t:
                list_t.append('-')
            else:
                list_t.append(res_t[0])

        return listA,list_t

    def __funds_list(self):
        """
        目前市场上所有成立的基金
        数据来源:http://fund.eastmoney.com/js/fundcode_search.js
        :return:
        """
        url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        resp = self.scrpy.request_method(url)
        return resp

    def __fund_request_by_code(self, code: str, flag: int = 1, method: int = 0, **kwargs):
        """
        通过传入基金code的方式根据功能自动拼接url获取数据
        :param code:fund代码列表
        :param flag:决定具体请求url.flag
            1. 基金主页    http://fund.eastmoney.com/xxx.html
            2. 实时净值    http://fundgz.1234567.com.cn/js/xxx.js
            3. 历史净值    http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=xxx&per=ddd&page=ppp
            4. 前十股票持仓 http://fundf10.eastmoney.com/ccmx_xxx.html
            5. 阶段涨幅    http://fundf10.eastmoney.com/jdzf_270002.html
            6. 季度年涨幅  http://fundf10.eastmoney.com/jndzf_270002.html
            7. 持有人结构  http://fundf10.eastmoney.com/cyrjg_270002.html
            8. 规模变动    http://fundf10.eastmoney.com/gmbd_270002.html
            9. 基金经理    http://fundf10.eastmoney.com/jjjl_270002.html
            10. 特殊数据   http://fundf10.eastmoney.com/tsdata_270002.html
        :param method:请求方式request/pyppeteer 0-request 1-pyppeterr
        :return:
        """
        url = self.__url_combine(flag, code, **kwargs)
        assert url, "url为空"
        self.logger.info(f"request url:[{url}])")
        if method == 0:  # request请求
            self.logger.info("request-method")
            resp = self.scrpy.request_method(url=url)

        elif method == 1:  # pyppeteer请求，获取动态js可以
            self.logger.info(f"pyppeteer-method.")
            resp = asyncio.get_event_loop().run_until_complete(self.scrpy.pyppeteer_method(url=url))
        else:
            self.logger.info(f"dont support this method.")
            return
        return resp

    def __json_to_dict(self, json_name: str = "fund_list.json"):
        """
        将json的格式转换为字典,方便后续处理
        :param json_name: 默认json文件名
        :return:
        """
        dict = json.load(open(json_name, 'r', encoding='utf-8'))
        if dict:
            return dict
        else:
            self.logger.info("json to dict failed.")

    def __url_combine(self, flag, code, **kwargs):
        """
        生成对应需要的url
        :param flag: 对应url的类型
            1. 基金主页    http://fund.eastmoney.com/xxx.html
            2. 实时净值    http://fundgz.1234567.com.cn/js/xxx.js
            3. 历史净值    http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=xxx&per=ddd&page=ppp
            4. 前十股票持仓 http://fundf10.eastmoney.com/ccmx_xxx.html
            5. 阶段涨幅    http://fundf10.eastmoney.com/jdzf_270002.html
            6. 季度年涨幅  http://fundf10.eastmoney.com/jndzf_270002.html
            7. 持有人结构  http://fundf10.eastmoney.com/cyrjg_270002.html
            8. 规模变动    http://fundf10.eastmoney.com/gmbd_270002.html
            9. 基金经理    http://fundf10.eastmoney.com/jjjl_270002.html
            10. 特殊数据   http://fundf10.eastmoney.com/tsdata_270002.html
        :param code: 基金代码
        :return:
        """
        if flag == 1:  # 天天基金主页
            fund_url = self._data_source_url.replace('xxx', code)
        elif flag == 2:  # 实时涨跌幅url
            fund_url = self._current_jjjz_url.replace('xxx', code)
        elif flag == 3:  # 历史净值rul
            if kwargs['day']:
                fund_url = self._history_jjjz_url.replace('xxx', code).replace('ddd', str(kwargs['day'])).\
                    replace('ppp',str(kwargs['page']))
        elif flag == 4:  # 基金股票持仓url
            fund_url = self._quote_hold_url.replace('xxx', code)
        elif flag == 5:  # 阶段涨幅
            fund_url = self._quote_hold_url.replace('ccmx_xxx','jdzf_' + code)
        elif flag == 6:  # 季度/年涨幅    _quote_hold_url = 'http://fundf10.eastmoney.com/ccmx_xxx.html'
            fund_url = self._quote_hold_url.replace('ccmx_xxx','jndzf_' + code)
        elif flag == 7:  # 持有人结构
            fund_url = self._quote_hold_url.replace('ccmx_xxx','cyrjg_' + code)
        elif flag == 8:  # 规模+规模变动
            fund_url = self._quote_hold_url.replace('ccmx_xxx','gmbd_' + code)
        elif flag == 9:  # 基金经理
            fund_url = self._quote_hold_url.replace('ccmx_xxx','jjjl_' + code)
        elif flag == 10:  # 特色数据
            fund_url = self._quote_hold_url.replace('ccmx_xxx','tsdata_' + code)
        else:
            self.logger.info("Unknown flag number,cant combine url.")
        self.logger.debug(f"__url_combine url:{fund_url}")
        return fund_url

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
        listA = [['序号', '代码', '名称', '股价', '涨跌幅', '占比', '万股数', '市值']]
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

    def list_to_dframe(self, la: list, index: list):
        """
        列表list转换为Dataframe格式数据
        :param la:
        :param index: 标题
        :return:
        """
        assert la and index,"la 和 index 不能为空"
        la_df = pd.DataFrame(data=la, columns=index)
        return la_df

    def csv_save(self, listA: list, title: list, csv_name: str = _current_day, mode: str = 'a+'):
        """
        数据存储进csv文件
        :param mode: 文件读写模式
        :rtype: object
        :param title: 标题
        :param listA:
        :param csv_name: 保存文件名
        :return:
        """
        self.logger.info(f"csv_file:{csv_name}")
        with open(csv_name, mode, encoding='utf-8-sig', newline='') as f:
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
                self.logger.info(row)  # row[0]
                # writer.writerows(row)
        self.logger.info(f"read csv:[{csv_name}] finish...")

    def db_save(self):
        """
        dataframe格式基金数据保存到DB数据库
        :return:
        """
        pass

    def db_read(self):
        """
        从DB读取某项数据
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
    fund_code_list = ['512000', '270002']
    ff = libFund(level=logging.INFO)
    # # 实时数据不作处理
    # # 获取基金列表的实时涨跌幅
    # ff.fund_current_jjjz()
    # #获取基金列表的持有收益率
    # ff.fund_rate_estimate()
    # # 获取基金列表的持有总金额和持有收益金额,实时估算收益
    # ff.fund_hold_info
    #
    # # 净值数据-
    # # 获取单个基金的历史几天的 单位净值 历史净值 日收益率
    # ff.fund_history_jjjz('512000', 1)

    # 可以存 xlsx和 DB
    # 格式：名称 代码 类型 xxx xxx ...
    # 全部基金列表: 名字 代码 类型 columns=['code','name','tpye']
    all_list = ff.funds_all_list(to_file=0)
    # for row in all_list.itertuples():
    #     print(getattr(row,'code'))
    #     print(getattr(row,'name'))
    #     print(getattr(row,'type'))
    print(all_list['name'][0])
    # 历史各种涨幅数据 : 共31项 1-阶段涨幅(10项) 2-季度涨幅(8个季度) 3-年度涨幅(8年) 4-持有人结构(最近一期的5项数据)
    sss1 = ff.fund_his_rates('270002')
    # 基础信息 : 规模变动信息（8个季度） + 基金经理任期管理信息（5项数据）
    sss2 = ff.fund_basic_info('270002')
    # 基金特色数据: 波动+夏普。
    sss3 = ff.fund_special_info('270002')

    sss4 = pd.concat([sss1,sss2,sss3])
    sss4.to_excel("sss4.xlsx")




