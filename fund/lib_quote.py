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


class libQuote(MyLogger):
    url_xxx = 'http://quote.eastmoney.com/xxxxxx.html'  # sz399001 # sz399006 #sh000001

    def __init__(self, level=logging.INFO):
        super().__init__(__name__, level)
        self.qs = libScrpy()

    @retry(2,3)
    def quote_all_info(self, code: list):  # turnover
        """
        获取页面所有信息
        :param code: 股票代码列表
        :return:
        """
        assert code, "股票代码必传"
        #  1.拼凑url
        la = []
        la.append(['名称', '代码', '当前价(点)', '涨跌幅', '涨跌额', '换手率', '成交量', '市盈', '成交额'])
        for i in range(len(code)):
            if code[i][0:3] == '000':
                curr_url = self.url_xxx.replace("xxxxxx", "sz" + code[i])
            if code[i][0:3] in ('600', '300'):
                curr_url = self.url_xxx.replace("xxxxxx", "sh" + code[i])

            #  2.发起请求
            text = asyncio.get_event_loop().run_until_complete(self.qs.pyppeteer_method(curr_url))
            #  3.匹配数据
            results = self.match_rule(text)
            #  4.转储数据
            la.append(results)

        for i in range(len(la)):
            self.logger.info(f"{la[i]}")
        return la

    def match_rule(self, content):
        """
        匹配规则
        :param content:网页内容
        :return:
        """
        assert content, "content不能为空"

        html = etree.HTML(content)

        xpath_rules = {
            1: '//*[@id="name"]/text()',    # 名称
            2: '//*[@id="code"]/text()',    # 代码
            3: '//*[@id="price9"]/text()',  # 当前价格(点数)
            4: '//*[@id="km2"]/text()',     # 当前涨跌幅度
            5: '//*[@id="km1"]/text()',     # 当前 涨跌额
            6: '//*[@id="gt4"]/text()',     # 换手率
            7: '//*[@id="gt5"]/text()',     # 成交量
            8: '//*[@id="gt6"]/text()',     # 市盈
            9: '//*[@id="gt12"]/text()'     # 成交额 gt12:股票类  指数类:gt11 gt1
        }

        lt = []
        for i in range(len(xpath_rules)):
            res = html.xpath(xpath_rules[i + 1])
            # self.logger.info(f"res[{i+1}]: {res[0]}")
            # if i + 1 == 6:
            #
            if i + 1 == 9:
                if '元' not in res:  # 不符合则代表为指数
                    res = html.xpath(xpath_rules[i + 1].replace('gt12', 'gt11'))
            if not res:
                lt.append(' ')
            else:
                lt.append(res[0])

        return lt


if __name__ == "__main__":
    quo = libQuote()
    code = ['000002', '000905']
    quo.quote_all_info(code)

"""
[2020-11-06 18:18:38] [INFO] [lib_quote.py quote_all_info 47] ['当前价(点)', '涨跌幅', '涨跌额', '换手率', '成交量', '市盈', '成交额']
[2020-11-06 18:18:38] [INFO] [lib_quote.py quote_all_info 47] ['6.76', '-2.73%', '-0.19', '2.74%', '18.42万手', '-11.61', '0.88']
[2020-11-06 18:18:38] [INFO] [lib_quote.py quote_all_info 47] ['3312.16', '-0.24%', '-7.97', '0.64%', '2.35亿手', ' ', '3255亿元']
"""