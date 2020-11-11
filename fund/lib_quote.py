# -*- coding: utf-8 -*-
"""
 @Topic:quote爬虫相关信息
    eg. 1.大盘各市实时成交总量
        2.关注的股票实时涨跌幅等信息
        3.
 @Date: 2020-11-5
 @Author: terry.wang
"""
from lib_scrpy import *
from lxml import etree
from lib_fund import retry
import tushare
import pandas as pd
import asyncio


class LibQuote(MyLogger):
    url_xxx = 'http://quote.eastmoney.com/xxxxxx.html'  # sz399001 # sz399006 #sh000001
    # 新浪财经数据下载链接
    his_data_url = 'http://quotes.money.163.com/service/chddata.html?code=0replace_code&end=replace_date' \
                   '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

    def __init__(self, level=logging.INFO):
        super().__init__(__name__, level)
        self.qs = libScrpy(level=logging.WARNING)

    @retry(2, 3)
    def quote_trade_info(self, code: list):  # turnover
        """
        股票实时交易信息获取(排除指数。。。)
        :param code: 股票代码列表
        :return:
        """
        assert code, "股票代码必传"
        la = []
        title = ['股票名称', '股票代码', '当前价', '涨跌幅', '涨跌额', '今开', '昨收', '最高', '最低', '涨停', '跌停', '换手率', '量比', '成交量', '成交额',
                 '市盈',
                 '市净', '总市值', '流通市值']
        for i in range(len(code)):
            #  1.拼凑url
            if code[i][0:3] in ('000', '002',
                                '300'):  # 深市000 中小板002 创业板300   http://quote.eastmoney.com/sz002002.html  http://quote.eastmoney.com/sz000002.html
                curr_url = self.url_xxx.replace("xxxxxx", 'sz' + code[i])
            elif code[i][0:3] in '600':  # 沪市600  http://quote.eastmoney.com/sh600600.html
                curr_url = self.url_xxx.replace("xxxxxx", 'sh' + code[i])
            elif code[i][0:3] in '688':  # 科创板688 http://quote.eastmoney.com/kcb/688300.html
                curr_url = self.url_xxx.replace("xxxxxx", '/kcb/' + code[i])
            else:
                self.logger.info(f"unknown code replace...[{curr_url}]")
                continue
            self.logger.info(f"curr_url is:[{curr_url}]")
            #  2.发起请求
            text = asyncio.get_event_loop().run_until_complete(self.qs.pyppeteer_method(curr_url))
            #  3.匹配数据
            results = self.__quote_match_rule(text)
            #  4.转储数据
            la.append(results)

        df_la = pd.DataFrame(la, columns=title)
        self.logger.info(df_la)

        return df_la

    def __quote_match_rule(self, content):
        """
        基本股票交易信息匹配规则
        :param content:网页内容
        :return:
        """
        assert content, "content不能为空"

        html = etree.HTML(content)
        xpath_rules = {
            1: '//*[@id="name"]/text()',  # 股票名称
            2: '//*[@id="code"]/text()',  # 股票代码
            3: '//*[@id="price9"]/text()',  # 当前价
            4: '//*[@id="km2"]/text()',  # 涨跌幅
            5: '//*[@id="km1"]/text()',  # 涨跌额
            6: '//*[@id="gt1"]/text()',  # 今开
            7: '//*[@id="gt8"]/text()',  # 昨收
            8: '//*[@id="gt2"]/text()',  # 最高
            9: '//*[@id="gt9"]/text()',  # 最低
            10: '//*[@id="gt3"]/text()',  # 涨停
            11: '//*[@id="gt10"]/text()',  # 跌停
            12: '//*[@id="gt4"]/text()',  # 换手率
            13: '//*[@id="gt11"]/text()',  # 量比
            14: '//*[@id="gt5"]/text()',  # 成交量
            15: '//*[@id="gt12"]/text()',  # 成交额
            16: '//*[@id="gt6"]/text()',  # 市盈
            17: '//*[@id="gt13"]/text()',  # 市净
            18: '//*[@id="gt17"]/text()',  # 总市值
            19: '//*[@id="gt14"]/text()'  # 流通市值
        }

        lt = []
        for i in range(len(xpath_rules)):
            res = html.xpath(xpath_rules[i + 1])
            if not res:
                lt.append(' ')
            else:
                lt.append(res[0])

        return lt

    @retry(2, 3)
    def zs_curr_info(self, code: list):
        """
        常用指数 所有实时信息
        @param code: 指数代码列表
        @return:
        """
        # http://quote.eastmoney.com/zs399005.html
        assert code, "指数代码必传"
        la = []
        title = ['指数名称', '指数代码', '当前点', '涨跌幅', '涨跌额', '今开', '昨收', '最高', '最低', '换手率', '振幅', '成交量', '成交额']
        for i in range(len(code)):
            try:
                #  1.拼凑指数url
                curr_url = self.url_xxx.replace("xxxxxx", 'zs' + code[i])
                self.logger.info(f"curr_url is:[{curr_url}]")
            except Exception as err_info:
                self.logger.info(f"Exception:err_info:[{err_info}].will continue.")
                continue
            #  2.发起请求
            text = asyncio.get_event_loop().run_until_complete(self.qs.pyppeteer_method(curr_url))
            #  3.匹配数据
            results = self.__zs_match_rule(text)
            #  4.转储数据
            la.append(results)

        df_la = pd.DataFrame(la, columns=title)
        self.logger.info(df_la)

        return la

    def __zs_match_rule(self, content):
        """
        指数匹配规则
        :param content:网页内容
        :return:
        """
        assert content, "content不能为空"

        html = etree.HTML(content)
        la = [['指数名称', '指数代码', '当前点', '涨跌幅', '涨跌额', '今开', '昨收', '最高', '最低', '换手率', '振幅', '成交量', '成交额']]
        xpath_rules = {
            1: '//*[@id="name"]/text()',  # 指数名称
            2: '//*[@id="code"]/text()',  # 指数代码
            3: '//*[@id="price9"]/text()',  # 当前点
            4: '//*[@id="km2"]/text()',  # 涨跌幅
            5: '//*[@id="km1"]/text()',  # 涨跌额
            6: '//*[@id="gt1"]/text()',  # 今开
            7: '//*[@id="gt7"]/text()',  # 昨收
            8: '//*[@id="gt2"]/text()',  # 最高
            9: '//*[@id="gt8"]/text()',  # 最低
            10: '//*[@id="gt4"]/text()',  # 换手率
            11: '//*[@id="gt10"]/text()',  # 振幅
            12: '//*[@id="gt5"]/text()',  # 成交量
            13: '//*[@id="gt11"]/text()',  # 成交额
        }

        lt = []
        for i in range(len(xpath_rules)):
            res = html.xpath(xpath_rules[i + 1])
            if not res:
                lt.append(' ')
            else:
                lt.append(res[0])

        return lt

    def quote_all_lists(self):
        """
        获取所有股票代码+名称
        :return:
        """
        pass

    def quote_info(self, code):
        """
        获取单只股票信息:to define
        :param code:
        :return:
        """
        pass

    def list_to_dframe(self, la: list, index: list):
        """
        列表list转换为 Dataframe 格式数据
        :param la:
        :param index: 标题
        :return:
        """
        assert la and index, "la 和 index 不能为空"
        la_df = pd.DataFrame(data=la, columns=index)

        return la_df


if __name__ == "__main__":
    quo = LibQuote()
    quo_code = ['002002', '000905', '600600', '688300']
    zs_code = ['000001', '399001', '399006']
    quo_trade_info = quo.quote_trade_info(quo_code)
    zs_info = quo.zs_curr_info(zs_code)
