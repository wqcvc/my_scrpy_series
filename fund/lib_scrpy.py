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
import os
import datetime
import logging
from fake_useragent import UserAgent
from pyppeteer import launch
import asyncio
from time import time

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s [%(pathname)s %(funcName)s %(lineno)d] %(message)s')
logger = logging.getLogger()


class libScrpy():
    _data_source_url = 'http://fund.eastmoney.com/xxx.html'
    # f"http://fund.eastmoney.com/{code}.html"
    # http: // fundf10.eastmoney.com / jjjz_270002.html
    _current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def __init__(self):
        pass

    def __url_combine(self, code):
        """
        根据code转换成对应的url
        :param code:
        :return:
        """
        fund_url = self._data_source_url.replace('xxx', code)
        logger.debug(f"__url_combine url:{fund_url}")
        return fund_url

    def single_request(self, code: str, method: int = 0):
        """
        单个
        :param code:fund代码
        :param method:请求方式request/pyppeteer
        :param url:单个url
        :return:
        """
        url = self.__url_combine(code)
        assert url, "url为空"
        if method == 0:
            logger.info("func:single_request in request-method")
            resp = self.request_method(url=url)

        elif method == 1:
            logger.info(f"func:single_request in pyppeteer-method.")
            resp = asyncio.get_event_loop().run_until_complete(self.pyppeteer_method(url=url))
        else:
            logger.info(f"func:single_request dont support this method.")
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
        logger.info(resp.status_code)

        if resp.status_code != 200:
            logger.info(f"Error url response status_code:{resp.status_code}")
            return

        end_time = time()
        logger.info(f"cost seconds:{end_time - start_time}")

        return resp

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
        resp = await page.goto(url=url,timeout=10000)
        logger.info(f"resp.status code:{resp.status}")
        if resp.status != 200:
            logger.info(f"Error resp.status code: {resp.status}.")
            return None
        text=await page.content()
        await browser.close()
        end_time = time()
        logger.info(f"cost seconds:{end_time - start_time}")

        return text

    def proxy_pool_set(self):
        """
        代理设置
        :return:
        """
        pass

# if __name__ == "__main__":
#     scrpp=libScrpy()
#     resp=scrpp.single_request('512000',1)
#     # resp=scrpp.single_request('512000')
#     # print(resp)
