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
from time import time
from lib_logger import MyLogger
import logging
import asyncio


class libScrpy(MyLogger):
    _current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def __init__(self, level=logging.INFO):
        super().__init__(__name__, level=level)

    def mult_request(self, urls: list):
        """
        一起
        :param urls:多个url
        :return:
        """
        pass

    def request_method(self, url):
        """
        使用正常的request库请求
        :return:
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
        resp.encoding = 'utf-8'
        self.logger.info(f"request status_code:[{resp.status_code}]")

        if resp.status_code != 200:
            self.logger.info(f"Error url response status_code:{resp.status_code}")
            return
        end_time = time()
        self.logger.info(f"this request cost seconds:{end_time - start_time}")

        return resp.text

    async def pyppeteer_method(self, url):
        """
        使用pyppeteer库可以请求到js数据
        :param url:
        :return:
        """
        start_time = time()
        ua = UserAgent()
        launch_args = {
            'headless': True,
            # 'devtools': False,  # 控制界面的显示，用来调试
            'args': [
                # "--start-maximized",
                '--no-sandbox',  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                # "--disable-infobars",
                # "--ignore-certificate-errors",
                # "--log-level=1",
                # "--disable-gpu",
                # "--disable-dev-shm-usage",
                # "--disable-software-rasterizer",
                # "--enable-extensions",
                # "--window-size=1920,1080",
                '--refer=http://fund.eastmoney.com',
                f'\"--user-agent={ua.random}\"',
            ],
            'dumpio': True,  # 解决浏览器多开卡死
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')
        resp = await page.goto(url=url, timeout=30000)
        self.logger.info(f"resp.status code:{resp.status}")
        if resp.status != 200:
            self.logger.info(f"Error resp.status code: {resp.status}.")
            return
        text = await page.content()
        await browser.close()
        end_time = time()
        self.logger.info(f"Request Costs:{end_time - start_time:.2f}s")
        return text

    def selenium_method(self,url: str):
        """
        selenium无头浏览器模式获取数据,原理和pyppeteer_method差不多,以后再实现
        :param url:
        :return:
        """
        pass

    def proxy_pool_set(self):
        """
        代理设置
        :return:
        """
        pass

    def save_to_file(self, content):
        """
        保存内容到文件
        :param content:
        :return:
        """
        pass

if __name__ == "__main__":
    scrpp = libScrpy()
    resp=scrpp.request_method(url='http://fundf10.eastmoney.com/tsdata_000002.html')
    # resp = asyncio.get_event_loop().run_until_complete(scrpp.pyppeteer_method(url='http://fundf10.eastmoney.com/tsdata_000002.html'))
    print(resp)
    # resp=scrpp.fund_request_by_code('512000')

