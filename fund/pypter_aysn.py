# coding=utf-8
# 测试pyppeteer 并发执行
import asyncio
from time import time
from pyppeteer import launch
from collections import namedtuple
from fake_useragent import UserAgent
import re
import requests
import pandas as pd
from lxml import etree

Response = namedtuple("rs", "title url html cookies headers history status")


def request_method(url):
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
    print(f"request status_code:[{resp.status_code}]")

    if resp.status_code != 200:
        print(f"Error url response status_code:{resp.status_code}")
        return
    end_time = time()
    # print(f"this request cost seconds:{end_time - start_time}")

    return resp.text

def __funds_list():
    """
    目前市场上所有成立的基金
    数据来源:http://fund.eastmoney.com/js/fundcode_search.js
    :return:
    """
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    resp = request_method(url)
    return resp

def funds_all_list(to_file: int = 0):
    """
    只取市场上所有开放基金的列表,存入xlsx
    :param to_file:是否写入xlsx文件
    :return:
    """
    resp = __funds_list()

    re_rule = {
        2: "\"(.*?)\",\".*?\",\"(.*?)\",\"(.*?)\",\".*?\""
    }

    re_res2 = re.findall(re_rule[2], str(resp))
    lpd = pd.DataFrame(re_res2, columns=['基金代码', '基金名称', '类型'])
    if to_file == 1:
        lpd.to_excel('all_funds.xlsx', index=False)
        print(f"all_funds write to xlsx file finish.")
    else:
        pass

    return lpd

async def get_html(rrs: list):
    la = funds_all_list()
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        la = la.iloc[rrs[0]:rrs[1]]
        la.index = range(len(la))
    # df_1, t1 = self.fund_his_rates(code_list)
    # df_2, t2 = self.fund_basic_info(code_list)
    # df_3, t3 = self.fund_special_info(code_list)

    res4_f = []
    url = 'http://fundf10.eastmoney.com/jdzf_xxxxx.html'
    for i in range(len(code_list)):
        start_time = time()
        ua = UserAgent()
        launch_args = {
            'headless': True,
            'args': [
                '--no-sandbox',  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                '--refer=http://fund.eastmoney.com',
                "--disable-infobars",
                "--ignore-certificate-errors",
                "--log-level=1",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "–-no-first-run",
                "–-no-zygote",
                "–-single-process"
                # "--enable-extensions",
                # "--window-size=1920,1080",
                f'\"--user-agent={ua.random}\"',
            ],
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')
        resp = await page.goto(url=url.replace('xxxxx',str(code_list[0])), timeout=30000)
        if resp.status != 200:
            return
        text = await page.content()
        await browser.close()
        end_time = time()
        print(f"this request cost seconds:{end_time - start_time}")
        # return text

        if text is None:
            return
        html = etree.HTML(text)
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
        res4_f.append(listA)
        # return listA
    df_f = pd.DataFrame(res4_f)
    # df_f.to_excel("fund_his_rates.xlsx")
    return df_f


async def get_html_1(url, timeout=10):
    # 默认30s
    print('---1')
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await  browser.newPage()
    res = await page.goto(url, options={'timeout': int(timeout * 1000)})
    # await asyncio.sleep(3)
    data = await page.content()
    title = await page.title()
    print('title 1= ', title)
    # resp_cookies = await page.cookies()
    # resp_headers = res.headers
    # resp_history = None
    # resp_status = res.status
    # response = Response(title=title, url=url,
    #                     html=data,
    #                     cookies=resp_cookies,
    #                     headers=resp_headers,
    #                     history=resp_history,
    #                     status=resp_status)
    # return response


if __name__ == '__main__':
    s_time = time()
    url_list = ["http://fundf10.eastmoney.com/jdzf_000179.html","http://fundf10.eastmoney.com/jndzf_000179.html","http://fundf10.eastmoney.com/tsdata_000204.html","http://fundf10.eastmoney.com/cyrjg_000179.html","http://fundf10.eastmoney.com/gmbd_000179.html","http://fundf10.eastmoney.com/jjjl_000179.html",

                ]  # , "http://www.10010.com/net5/011/", "http://python.jobbole.com/87541/"

    # tasks = [get_html(url_list[0]), get_html(url_list[1]), get_html(url_list[2]), get_html(url_list[3]), get_html(url_list[4]),get_html(url_list[5])]
    tasks = [ get_html(rrs=[0,3]),get_html(rrs=[3,6]),get_html(rrs=[6,9])]

    loop = asyncio.get_event_loop()

    # loop.run_until_completrun_until_completee(get_html(url_list[0]))
    # loop.(get_html(url_list[1]))
    # loop.run_until_complete(get_html(url_list[2]))
    # loop.run_until_complete(get_html(url_list[3]))
    # loop.run_until_complete(get_html(url_list[4]))

    # results = loop.run_until_complete(asyncio.gather(*task))
    # tasks = [(get_html(url)) for url in url_list]
    # cost 24s
    # results = loop.run_until_complete(asyncio.wait(tasks))  # loop.run_until_complete() 既可以接收一个协程对象, 也可以接收一个 future 对象
    # cost 23s
    results = loop.run_until_complete(asyncio.gather(*tasks))  # loop.run_until_complete() 既可以接收一个协程对象, 也可以接收一个 future 对象

    # # cost 35s
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[0]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[1]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[2]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[3]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[4]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[5]))

    # loop.close()

    # for res in results:
    #     print(res.title,res.url)
    print(results)

    print('耗时：', time() - s_time)
