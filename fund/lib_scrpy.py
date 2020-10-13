# -*- coding: utf-8 -*-
"""
 @Topic:爬取的相关:
        1.数据获取
        2.数据处理
        3.数据存储...
 @Date: 2020-9-15
 @Author: terry.wang
"""
import requests
import datetime
from fake_useragent import UserAgent
from pyppeteer import launch
import asyncio
from time import time
from lib_logger import MyLogger
import logging


class libScrpy(MyLogger):
    _data_source_url = 'http://fund.eastmoney.com/xxx.html'
    _current_jjjz_url='http://fundgz.1234567.com.cn/js/xxx.js'
    _history_jjjz_url='http://fundf10.eastmoney.com/jjjz_xxx.html'
    # http: // fundf10.eastmoney.com / jjjz_270002.html
    _current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def __init__(self,level=logging.INFO):
        super().__init__(__name__,level=level)
        # self.logger=MyLogger("libScrpy")

    def __url_combine(self, flag, code):
        """
        生成对应需要的url
        :param flag: 对应url的类型 1:_data_source_url基金主页 2:_current_jjjz_url实时净值 3:_history_jjjz_url历史净值
        :param code: 基金代码
        :return:
        """
        if flag == 1:
            fund_url = self._data_source_url.replace('xxx', code)
        elif flag == 2:
            fund_url = self._current_jjjz_url.replace('xxx', code)
        elif flag == 3:
            fund_url = self._history_jjjz_url.replace('xxx', code)
        else:
            self.logger.info("Unknown flag number,not Url.")
        self.logger.debug(f"__url_combine url:{fund_url}")
        return fund_url

    def single_request(self, code: str, flag: int = 1, method: int = 0):
        """
        单个请求
        :param code:fund代码
        :param flag:决定具体请求url.对应url的类型 1:_data_source_url基金主页 2:_current_jjjz_url实时净值 3:_history_jjjz_url历史净值
        :param method:请求方式request/pyppeteer
        :param url:单个url
        :return:
        """
        url = self.__url_combine(flag,code)
        assert url, "url为空"
        self.logger.info(f"request url:[{url}])")
        if method == 0:  # request请求
            self.logger.info("request-method")
            resp = self.request_method(url=url)

        elif method == 1:  # pyppeteer请求，获取动态js可以
            self.logger.info(f"pyppeteer-method.")
            resp = asyncio.get_event_loop().run_until_complete(self.pyppeteer_method(url=url))
        else:
            self.logger.info(f"dont support this method.")
            return
        return resp

    def mult_request(self, urls: list):
        """
        一起
        :param urls:多个url
        :return:
        """
        pass

    def request_method(self, url):
        """
        使用request库
        :param url:
        :return:
        """
        ua = UserAgent()
        headers = {
            'refer': 'http://fund.eastmoney.com/',
            'User-Agent': ua.random
        }
        start_time = time()
        resp = requests.request(method="GET", url=url, headers=headers)
        resp.encoding='utf-8'
        self.logger.info(f"request status_code:[{resp.status_code}]")

        if resp.status_code != 200:
            self.logger.info(f"Error url response status_code:{resp.status_code}")
            return

        end_time = time()
        self.logger.info(f"this request cost seconds:{end_time - start_time}")
        return resp.text

    async def pyppeteer_method(self, url):
        """
        使用pyppeteer库
        :param url:
        :return:
        """
        start_time = time()
        ua = UserAgent()
        launch_args = {
            "headless": True,
            'devtools': False,  # 控制界面的显示，用来调试
            "args": [
                "--start-maximized",
                "--no-sandbox",  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                "--disable-infobars",
                "--ignore-certificate-errors",
                "--log-level=3",
                "--enable-extensions",
                "--window-size=1920,1080",
                "--refer=http://fund.eastmoney.com",
                f"\"--user-agent={ua.random}\"",
            ],
            'dumpio': True,  # 解决浏览器多开卡死
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        resp = await page.goto(url=url, timeout=10000)
        self.logger.info(f"resp.status code:{resp.status}")
        if resp.status != 200:
            self.logger.info(f"Error resp.status code: {resp.status}.")
            return None
        text = await page.content()
        await browser.close()
        end_time = time()
        self.logger.info(f"this request cost seconds:{end_time - start_time}")

        return text

    def proxy_pool_set(self):
        """
        代理设置
        :return:
        """
        pass

    def save_to_file(self,content):
        """
        保存内容到文件
        :param content:
        :return:
        """
        pass

# if __name__ == "__main__":
#     scrpp=libScrpy()
#     resp=scrpp.single_request('512000',1)
#     # resp=scrpp.single_request('512000')
#     # print(resp)
