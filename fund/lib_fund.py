# -*- coding: utf-8 -*-
"""
 @Topic:fund相关操作和数据
  useage：
    1.获取基金列表的实时涨跌幅
      ff.fund_current_jjjz()
    2.获取基金列表的持有收益率
      ff.fund_rate_estimate()
    3.获取基金列表的持有总金额 + 持有收益金额 + 实时估算收益
      ff.fund_hold_info
    4.单个基金股票前10数据 + 仓位占比重
      ff.fund_hold_shares('163406')
    5.单个基金的历史单位净值 + 历史净值 + 日收益率
      ff.fund_history_jjjz('512000', 1)
    6.全部基金列表: 基金名字 基金代码 类型
      all_list = ff.funds_all_list(to_file=0)
    7.历史各种涨幅数据 : 共31项 1-阶段涨幅(10项) 2-季度涨幅(8个季度) 3-年度涨幅(8年) 4-持有人结构(最近一期的5项数据)
      sss1 = ff.fund_his_rates(['270002','161219'])
    8.基础信息 : 规模变动信息（8个季度） + 基金经理任期管理信息（5项数据）
      sss2 = ff.fund_basic_info(['270002','161219'])
    9.基金特色数据: 标准差 + 夏普率。
      sss3 = ff.fund_special_info(['000002'])
    10.基金汇总保存进同一个csv + xlsx. 可以不连续请求。eg: 0:2 2:5 5:10分段
    (重要：次函数存在性能问题。需要使用此功能请关注同目录下的 pypter_aysn.py 使用了协程异步请求，极大提高了请求效率)
      ff.funds_full_info([0, 6945])
    11.存储进mysql 和 读取出来
      ff.db_save()/db_read()
    12.定期更新数据库内容
      to do
    13.to be continue...图形界面 or web 展示，使用 vue or flask django
    14.基金公司排名+规模等信息
    15.画图 pandas matlab
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
import threading
import sys
from sqlalchemy import event, exc, select, orm, create_engine
from urllib.parse import quote_plus


# 装饰器:执行时间统计
def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(f"函数名:[{func.__name__}]执行耗时:[{t2 - t1:.2f}]秒.")

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

    _current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
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
        self.name, self.gszzl, self.gsz, self.dwjz = [], [], [], []
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

        codes, costs, numbers = [], [], []
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
        df_hisjz = pd.DataFrame(hisjz_list, columns=['净值日期', '单位净值', '累计净值', '日增长率'])
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

        x = 0.0
        for i in range(len(quote_info_list)):
            self.logger.info(f"[{i + 1}]:{quote_info_list[i]}")
            if i != 0:
                x += float(quote_info_list[i][5].replace('%', ''))
        self.logger.info(f"前十重仓占比总仓位比例:[{x:.2f}]")

        """
        to do: 前10股票占比例
        """

        return quote_info_list

    def fund_company_info(self):
        """
        返回所有基金公司的各种信息:名字 规模 成立日期 排名等
        :return:
        """
        url = "http://fund.eastmoney.com/company/default.html"
        resp = asyncio.get_event_loop().run_until_complete(self.scrpy.pyppeteer_method(url=url))
        df_cominfo = self.__re_company_info(resp)

        df_f = pd.DataFrame(df_cominfo, columns=['基金公司', '成立时间', '全部管理规模(亿)', '全部基金数', '全部经理数'])
        self.logger.info(df_f)
        return df_f

    def __re_company_info(self, content):
        """
        使用xpath匹配基金公司排名
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="gspmTbl"]/tbody/tr[1]/td[2]/a/text()',  # 公司名字  //*[@id="gspmTbl"]/tbody/tr[2]/td[2]/a tr+
            2: '//*[@id="gspmTbl"]/tbody/tr[1]/td[4]/text()',  # 成立时间   //*[@id="gspmTbl"]/tbody/tr[2]/td[4]
            3: '//*[@id="gspmTbl"]/tbody/tr[1]/td[6]/p/text()',  # 管理规模   //*[@id="gspmTbl"]/tbody/tr[2]/td[6]/p/text()
            4: '//*[@id="gspmTbl"]/tbody/tr[1]/td[7]/a/text()',  # 管理数量
            5: '//*[@id="gspmTbl"]/tbody/tr[1]/td[8]/a/text()'  # 经理数量
        }
        # 基金公司全排名。共 159家公司
        listA = []
        for i in range(159):
            list_t = []
            for k in range(len(xpath_rules)):
                res = html.xpath(xpath_rules[k+1].replace('tr[1]', f"tr[{i + 1}]"))
                if not res:
                    listA.append('-')
                else:
                    list_t.append(res[0])
            listA.append(list_t)
        return listA

    def fund_his_rates(self, code: list):
        """
        各种涨幅
        :param code: 基金代码
        :param  : 涨幅: 1-阶段涨幅 2-季度涨幅 3-年度涨幅 4-持有人结构
        :return:
        """
        # 阶段涨幅   http://fundf10.eastmoney.com/jdzf_270002.html
        # 季度年涨幅  http://fundf10.eastmoney.com/jndzf_270002.html
        # 持有人结构  http://fundf10.eastmoney.com/cyrjg_270002.html

        res4_f, res1_t, res2_t, res3_t = [], [], [], []
        flag = 0
        for i in range(len(code)):
            self.logger.info(
                f"In func[{sys._getframe().f_code.co_name}]的第[{i + 1}]个/共{len(code)}个 : current code:[{code[i]}]")
            # 阶段涨幅
            content1 = self.__fund_request_by_code(code=code[i], flag=5, method=1)
            # 返回为Nonetype时候的处理
            res1 = self.__re_fund_jdzf(content=content1)
            # 提高性能优化标题re次数
            # self.logger.info(f"res1 is:{res1}")
            if not res1:
                res1 = ['未获取'] * 10
            if flag == 0:
                content_t1 = self.__fund_request_by_code(code='000001', flag=5, method=1)
                res1_t = self.__re_fund_jdzf_title(content=content_t1)
            # 季度/年涨幅
            content2 = self.__fund_request_by_code(code=code[i], flag=6, method=1)
            res2 = self.__re_fund_jndzf(content=content2)
            # self.logger.info(f"res2 is:{res2}")
            if not res2:
                res2 = ['未获取'] * 16
            if flag == 0:
                content_t2 = self.__fund_request_by_code(code='000001', flag=6, method=1)
                res2_t = self.__re_fund_jndzf_title(content=content_t2)
            # 持有人结构
            content3 = self.__fund_request_by_code(code=code[i], flag=7, method=1)
            res3 = self.__re_fund_cyrjg(content=content3)
            # self.logger.info(f"res3 is:{res3}")
            if not res3:
                res3 = ['未获取'] * 5
            if flag == 0:
                content_t3 = self.__fund_request_by_code(code='000001', flag=7, method=1)
                res3_t = self.__re_fund_cyrjg_title(content=content_t3)
            res4_f.append(res1 + res2 + res3)
            flag += 1

        res_f_t = res1_t + res2_t + res3_t
        df_f = pd.DataFrame(res4_f, columns=res_f_t)
        # df_f.to_excel("fund_his_rates.xlsx")
        return df_f, res_f_t

    def fund_basic_info(self, code: list):
        """
        基金规模数据+基金经理信息
        :param code:
        :param : 1.规模+规模增长数据 2.基金经理个人,管理规模,业绩等信息
        :return:
        """
        res_f, res1_t, res2_t = [], [], []
        flag = 0
        for i in range(len(code)):
            self.logger.info(
                f"In func[{sys._getframe().f_code.co_name}]的第[{i + 1}]个/共{len(code)}个 : current code:[{code[i]}]")
            # 规模变动  http://fundf10.eastmoney.com/gmbd_270002.html
            content1 = self.__fund_request_by_code(code=code[i], flag=8, method=1)
            res1 = self.__re_fund_gmbd(content=content1)
            if not res1:
                res1 = ['未获取'] * 8
            if flag == 0:
                content_t1 = self.__fund_request_by_code(code='000001', flag=8, method=1)
                res1_t = self.__re_fund_gmbd_title(content=content_t1)

            # 基金经理  http://fundf10.eastmoney.com/jjjl_270002.html
            content2 = self.__fund_request_by_code(code=code[i], flag=9, method=1)
            res2 = self.__re_fund_jjjl(content=content2)
            if not res2:
                res2 = ['未获取'] * 6
            if flag == 0:
                content_t2 = self.__fund_request_by_code(code='000001', flag=9, method=1)
                res2_t = self.__re_fund_jjjl_title(content=content_t2)
            res_f.append(res1 + res2)
            flag += 1

        res_f_t = res1_t + res2_t
        df_f = pd.DataFrame(res_f, columns=res_f_t)
        # df_f.to_excel("fund_basic_info.xlsx")
        return df_f, res_f_t

    def fund_special_info(self, code: list):
        """
        基金特色数据
        :param code:
        :param : 1.近1年夏普比率  2.近1年波动率 3.近1年最大回撤 4.近1年最大回撤率
        :return:
        """
        # 特殊数据 http://fundf10.eastmoney.com/tsdata_270002.html
        res_f, res1_t = [], []
        flag = 0
        for i in range(len(code)):
            self.logger.info(
                f"In func[{sys._getframe().f_code.co_name}]的第[{i + 1}]个/共{len(code)}个 : current code:[{code[i]}]")
            content1 = self.__fund_request_by_code(code=code[i], flag=10, method=1)
            res1 = self.__re_fund_tsdata(content=content1)
            if not res1:
                res1 = ['未获取'] * 2
            if flag == 0:
                content_t1 = self.__fund_request_by_code(code='000001', flag=10, method=1)
                res1_t = self.__re_fund_tsdata_title(content=content_t1)
            res_f.append(res1)
            flag += 1

        df_f = pd.DataFrame(res_f, columns=res1_t)
        # df_f.to_excel("fund_special_info.xlsx")

        return df_f, res1_t

    def funds_all_list(self, to_file: int = 0):
        """
        只取市场上所有开放基金的列表,存入xlsx
        :param to_file:是否写入xlsx文件
        :return:
        """
        resp = self.__funds_list()

        re_rule = {
            2: "\"(.*?)\",\".*?\",\"(.*?)\",\"(.*?)\",\".*?\""
        }

        re_res2 = re.findall(re_rule[2], str(resp))
        lpd = pd.DataFrame(re_res2, columns=['基金代码', '基金名称', '类型'])
        if to_file == 1:
            lpd.to_excel('funds_all_list.xlsx', index=False)
            self.logger.info(f"all_funds write to xlsx file finish.")
        else:
            pass

        return lpd

    @timer
    def funds_full_info(self, rrs: list = None):
        """
        所有基金相关信息统一函数：统一请求并写入文件
        rrs:每次请求的范围。可以重复多次写入 funds_full_info.csv文件中
        @return:
        """
        la = self.funds_all_list(to_file=1)
        # 过滤去除没用的 债券型和固收等类型的基金
        dd = la[la.类型.isin(
            ['混合型', '联接基金', 'QDII', '股票指数', 'QDII-指数', 'ETF-场内', 'QDII-ETF', '分级杠杆', '股票-FOF', '股票型', '混合-FOF'])]
        dd.to_excel('funds_use_list.xlsx', index=False)
        code_list = dd['基金代码'].tolist()
        if rrs:
            code_list = code_list[rrs[0]:rrs[1]]
            # 复制并更新索引
            dd = dd.iloc[rrs[0]:rrs[1]]
            dd.index = range(len(dd))
        df_1, t1 = self.fund_his_rates(code_list)
        df_2, t2 = self.fund_basic_info(code_list)
        df_3, t3 = self.fund_special_info(code_list)

        # 合并数据写入funds_full_info.csv
        fal = pd.concat([dd, df_1, df_2, df_3], axis=1)
        fal.to_csv('funds_full_info.csv', mode='a+', index=False, header=False)

        # 转存xlsx+标题.写入xlsx失败没关系。csv有完整数据，再次保存进xlsx即可
        # 如果出现: Duplicate names are not allowed. 说明colnums中有很多重复的字段，例如: - 。截取的code没有数据导致
        colnums = ['基金代码', '基金名称', '类型'] + t1 + t2 + t3
        self.logger.info(colnums)
        fal_f = pd.read_csv('funds_full_info.csv', names=colnums, dtype=str)
        self.logger.info(fal_f)
        excel_name = 'funds_full_info.xlsx'
        fal_f.to_excel(excel_name)

    def update_funds_mysqldata(self):
        """
        更新mysql基金的数据 : 1.只更新全部or部分字段数据:季度涨幅等  2.新基金加入  3.xxx
        :return:
        """
        ...

    def __re_fund_jdzf(self, content):
        """
        使用xpath匹配基金的阶段涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="jdzftable"]/div/ul[2]/li[2]/text()',  # 今年来  近1周  近1，3，6个月  近1，2，3，5年 成立以来 ul+
            2: '//*[@id="jdzftable"]/div/ul[2]/li[1]/text()'  # 标题 ul+
        }

        listA = []
        for i in range(10):
            res = html.xpath(xpath_rules[1].replace('ul[2]', f"ul[{i + 2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
        return listA

    def __re_fund_jdzf_title(self, content):
        """
        使用xpath匹配基金的阶段涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            2: '//*[@id="jdzftable"]/div/ul[2]/li[1]/text()'  # 标题 ul+
        }

        list_t = []
        for i in range(10):
            res2 = html.xpath(xpath_rules[2].replace('ul[2]', f"ul[{i + 2}]"))
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])
        return list_t

    def __re_fund_jndzf(self, content):
        """
        使用xpath匹配基金的季度/年涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="quarterzftable"]/table/tbody/tr[1]/td[2]/text()',  # 季度涨幅 td+
            2: '//*[@id="yearzftable"]/table/tbody/tr[1]/td[2]/text()'  # 年度涨幅 td+
        }

        # 最近8个季度的涨幅
        listA = []
        for i in range(8):
            res = html.xpath(xpath_rules[1].replace('td[2]', f"td[{i + 2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])

        # 最近8年的业绩
        for i in range(8):
            res = html.xpath(xpath_rules[2].replace('td[2]', f"td[{i + 2}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])

        return listA

    def __re_fund_jndzf_title(self, content):
        """
        使用xpath匹配基金的季度/年涨幅
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            3: '//*[@id="quarterzftable"]/table/thead/tr/th[2]/text()',  # 季度标题 th+
            4: '//*[@id="yearzftable"]/table/thead/tr/th[2]/text()'  # 年度标题 th+
        }
        list_t = []
        for i in range(8):
            res2 = html.xpath(xpath_rules[3].replace('th[2]', f"th[{i + 2}]"))
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])
        for i in range(8):
            res2 = html.xpath(xpath_rules[4].replace('th[2]', f"th[{i + 2}]"))
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])

        return list_t

    def __re_fund_cyrjg(self, content):
        """
        使用xpath匹配基金的持有人结构
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="cyrjgtable"]/table/tbody/tr[1]/td[1]/text()',  # 只要最近更新的一期结构中 各占比例即可。 日期 机构 个人 内部 总份额 td+
        }

        listA = []
        for i in range(5):
            res = html.xpath(xpath_rules[1].replace('td[1]', f"td[{i + 1}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])

        return listA

    def __re_fund_cyrjg_title(self, content):
        """
        使用xpath匹配基金的持有人结构
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            2: '//*[@id="cyrjgtable"]/table/thead/tr/th[1]/text()'  # 标题 th+

        }

        list_t = []
        for i in range(5):
            res2 = html.xpath(xpath_rules[2].replace('th[1]', f"th[{i + 1}]"))
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])
        return list_t

    def __re_fund_gmbd(self, content):
        """
        使用xpath匹配基金的规模变动
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="gmbdtable"]/table/tbody/tr[1]/td[5]/text()',
            # 最近8期的规模变动 tr+ //*[@id="gmbdtable"]/table/tbody/tr[2]/td[5]
        }

        listA = []
        # 最近8个季度的规模变动信息
        for i in range(8):
            res = html.xpath(xpath_rules[1].replace('tr[1]', f"tr[{i + 1}]"))
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
        return listA

    def __re_fund_gmbd_title(self, content):
        """
        使用xpath匹配基金的规模变动
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            2: '//*[@id="gmbdtable"]/table/tbody/tr[1]/td[1]/text()'
            # 标题 tr+   //*[@id="gmbdtable"]/table/tbody/tr[2]/td[1]
        }

        list_t = []
        # 最近8个季度的规模变动信息
        for i in range(8):
            res2 = html.xpath(xpath_rules[2].replace('tr[1]', f"tr[{i + 1}]"))
            if not res2:
                list_t.append('-')
            else:
                list_t.append(res2[0])
        return list_t

    def __re_fund_jjjl(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[1]/text()',  # 起始期
            2: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[2]/text()',  # 截止期
            3: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[3]/a/text()',  # 基金经理
            4: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/text()',  # 任职时间
            5: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[5]/text()',  # 任职回报
            6: '//*[@id="bodydiv"]/div[8]/div[3]/div[1]/div[2]/p/label[1]/span/text()'  # 基金成立日期
        }

        listA = []
        # 最近1个经理任期业绩 6项数据
        for i in range(6):
            res = html.xpath(xpath_rules[i + 1])
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])

        return listA

    def __re_fund_jjjl_title(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return
        html = etree.HTML(content)
        xpath_rules = {
            6: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/table/thead/tr/th[1]/text()',  # 标题
            7: '//*[@id="bodydiv"]/div[8]/div[3]/div[1]/div[2]/p/label[1]/text()'  # 成立日期标题
        }

        list_t = []
        # 最近1个经理任期业绩 5项数据标题 + 成立日期标题
        for i in range(5):
            res_t = html.xpath(xpath_rules[6].replace('th[1]', f"th[{i + 1}]"))
            if not res_t:
                list_t.append('-')
            else:
                list_t.append(res_t[0])
        res_t2 = html.xpath(xpath_rules[7])
        if res_t2:
            res_t2 = res_t2[0].replace('：', '')
            list_t.append(res_t2)
        else:
            list_t.append('-')

        return list_t

    def __re_fund_tsdata(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return ['-', '-']
        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[2]/td[2]/text()',
            # 近1年标注差
            2: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[3]/td[2]/text()',
            # 近1年夏普率
        }
        listA = []
        # 最近1个经理任期业绩
        for i in range(len(xpath_rules)):
            res = html.xpath(xpath_rules[i + 1])
            if not res:
                listA.append('-')
            else:
                listA.append(res[0])
        return listA

    def __re_fund_tsdata_title(self, content):
        """
        使用xpath匹配基金的基金经理信息等
        :param content: 网页内容，需要解析的
        :return:
        """
        if content is None:
            return ['-', '-']
        html = etree.HTML(content)
        xpath_rules = {
            3: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[2]/td[1]/text()',
            # 标准差 title td
            4: '//*[@id="bodydiv"]/div[8]/div[3]/div[2]/div[3]/div/div[1]/div/div[4]/table/tbody/tr[3]/td[1]/text()',
            # 夏普率
        }
        list_t = []
        for i in range(len(xpath_rules)):
            res_t = html.xpath(xpath_rules[i + 3])
            if not res_t:
                list_t.append('-')
            else:
                list_t.append(res_t[0])
        return list_t

    def __funds_list(self):
        """
        目前市场上所有成立的基金
        数据来源:http://fund.eastmoney.com/js/fundcode_search.js
        :return:
        """
        url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        resp = self.scrpy.request_method(url)
        return resp

    @retry(2, 5)
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
            resp = asyncio.get_event_loop().run_until_complete(self.scrpy.pyppeteer_method(url=url))
            # loop = asyncio.new_event_loop().run_until_complete(self.scrpy.pyppeteer_method(url=url))
            # asyncio.set_event_loop(loop)
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
                fund_url = self._history_jjjz_url.replace('xxx', code).replace('ddd', str(kwargs['day'])). \
                    replace('ppp', str(kwargs['page']))
        elif flag == 4:  # 基金股票持仓url
            fund_url = self._quote_hold_url.replace('xxx', code)
        elif flag == 5:  # 阶段涨幅
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'jdzf_' + code)
        elif flag == 6:  # 季度/年涨幅    _quote_hold_url = 'http://fundf10.eastmoney.com/ccmx_xxx.html'
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'jndzf_' + code)
        elif flag == 7:  # 持有人结构
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'cyrjg_' + code)
        elif flag == 8:  # 规模+规模变动
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'gmbd_' + code)
        elif flag == 9:  # 基金经理
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'jjjl_' + code)
        elif flag == 10:  # 特色数据
            fund_url = self._quote_hold_url.replace('ccmx_xxx', 'tsdata_' + code)
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
        re_res = re.findall(re_rule[1].replace('xxxxxx', code), str(resp))
        if re_res[0]:
            code_name = re_res[0]

        return code_name

    def list_to_dframe(self, la: list, columns: list):
        """
        列表list转换为Dataframe格式数据
        :param la:
        :param index: 标题
        :return:
        """
        assert la and columns, "la 和 columns标题 不能为空"
        la_df = pd.DataFrame(data=la, columns=columns)
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

    def db_save(self, dffile, totable, **configs):
        """
        dataframe格式基金数据完整保存到DB数据库
        @param dffile: xlsx数据文件
        @param totable: 存储到的数据库表table
        @param configs: 连接数据库的配置，不传有默认本地配置
        @return:
        """
        username = configs.get('username', 'root')
        password = configs.get('password', 'km9m77wq123')
        host = configs.get('host', '127.0.0.1')
        assert host, 'host必填'
        port = configs.get('port', '3306')
        db = configs.get('db', 'fund') or configs.get('schema', 'fund')
        if_exists = configs.get('if_exists', 'replace')
        index = configs.get('index', False)
        engine = create_engine(f"mysql+pymysql://{username}:{quote_plus(password)}@{host}:{port}/{db}?charset=utf8",
                               echo=True,  # echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
                               pool_size=10,  # pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
                               pool_recycle=60 * 2,  # pool_recycle: 设置时间以限制数据库多久没连接自动断开
                               pool_pre_ping=True
                               )
        # 2. pandas write to sql
        df2 = pd.read_excel(dffile, dtype=str)
        # 不储存index列.且table存在则 覆盖 写入
        df2.to_sql(totable, engine, index=index, schema=db, if_exists=if_exists)
        self.logger.info(f"write to db:[{db}:{totable}] success.!!!")

    def db_read(self, selectable, **configs):
        """
        基金数据从DB数据库全读取出来 返回dataframe格式
        @param selectable: 读取的数据库表名
        @param configs: 连接数据库的配置，不传有默认本地配置
        @return:
        """
        username = configs.get('username', 'root')
        password = configs.get('password', 'km9m77wq123')
        host = configs.get('host', '127.0.0.1')
        assert host, 'host必填'
        port = configs.get('port', '3306')
        db = configs.get('db', 'fund') or configs.get('schema', 'fund')
        engine = create_engine(f"mysql+pymysql://{username}:{quote_plus(password)}@{host}:{port}/{db}?charset=utf8",
                               echo=True,  # echo: 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
                               pool_size=10,  # pool_size: 连接池的大小，默认为5个，设置为0时表示连接无限制
                               pool_recycle=60 * 2,  # pool_recycle: 设置时间以限制数据库多久没连接自动断开
                               pool_pre_ping=True
                               )
        # 1. pandas read sql
        configs.get('sql')
        query_sql = f'''
         select * from {db}.{selectable};
         '''
        df = pd.read_sql_query(query_sql, engine)
        self.logger.info(df)
        self.logger.info(df.iloc[0, 1])
        return df

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

    # # 1.获取基金列表的实时涨跌幅
    # ff.fund_current_jjjz()
    # # 2.获取基金列表的持有收益率
    # ff.fund_rate_estimate()
    # # 3.获取基金列表的持有总金额 + 持有收益金额 + 实时估算收益
    # ff.fund_hold_info
    # # 4.单个基金股票前10数据 + 仓位占比重
    # ff.fund_hold_shares('163406')
    # # 5.单个基金的历史单位净值 + 历史净值 + 日收益率
    # ff.fund_history_jjjz('512000', 1)
    # # 6.全部基金列表: 基金名字 基金代码 类型
    # all_list = ff.funds_all_list(to_file=0)
    # print(all_list['name'][0])
    # # 7.历史各种涨幅数据 : 共31项 1-阶段涨幅(10项) 2-季度涨幅(8个季度) 3-年度涨幅(8年) 4-持有人结构(最近一期的5项数据)
    # sss1 = ff.fund_his_rates(['270002', '161219'])
    # # 8.基础信息 : 规模变动信息（8个季度） + 基金经理任期管理信息（5项数据）
    # sss2 = ff.fund_basic_info(['270002', '161219'])
    # # 9.基金特色数据: 标准差 + 夏普率。
    # sss3 = ff.fund_special_info(['000002'])
    # # 10.基金汇总保存进同一个csv + xlsx. 可以不连续请求。eg: 0:2 2:5 5:10分段
    # # 存在性能问题目前,使用 pypter_aysn.py协程并发极大提高效率。i5 cpu大概 27小时能更新完数据。之前需要100多个小时
    # ff.funds_full_info([0, 6945])  # 20个400多s 10个200多s 20个720s
    # # 11.保存数据库
    # sourcefile1 = 'funds_use_list.xlsx'
    # dstable1 = 'funds_use_list'
    # ff.db_save(dffile=sourcefile1, totable=dstable1, host='127.0.0.1', schema='fund')
    # sourcefile2 = 'funds_full_info.xlsx'
    # dstable2 = 'funds_full_info'
    # ff.db_save(dffile=sourcefile2, totable=dstable2)
    # # 12.从数据库读取数据
    # table = 'funds_full_info'
    # df_f_db = ff.db_read(selectable=table, schema='fund')

    # 13.基金公司排名+管理规模等信息
    cominfo = ff.fund_company_info()
    sourcefile3 = 'funds_company_info.xlsx'
    dstable3 = 'funds_company_info'
    cominfo.to_excel(sourcefile3)
    ff.db_save(dffile=sourcefile3, totable=dstable3, host='127.0.0.1', schema='fund')
