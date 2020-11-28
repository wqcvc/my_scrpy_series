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
import inspect
import functools
import sys

Response = namedtuple("rs", "title url html cookies headers history status")


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
    print(f"Request costs :{end_time - start_time:.2f}s")

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

    dd = lpd[lpd.类型.isin(
        ['混合型', '联接基金', 'QDII', '股票指数', 'QDII-指数', 'ETF-场内', 'QDII-ETF', '分级杠杆', '股票-FOF', '股票型', '混合-FOF'])]
    dd.to_excel('funds_use_list.xlsx', index=False)
    return dd

la = funds_all_list()

@retry(2, 5)
async def get_jdzf(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    print(f"code_list length is: [{len(code_list)}]")
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/jdzf_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            # return text

            if text is None:
                res4_f.append(['未获取'] * 10)
                continue
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
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
        # return listA
    df_f = pd.DataFrame(res4_f)
    # df_f.to_excel("fund_his_rates.xlsx")
    return df_f

@retry(2, 5)
async def get_jndzf(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/jndzf_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                print(f"resp.status: [{resp.status}]")
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            # return text

            if text is None:
                res4_f.append(['未获取'] * 16)
                continue
            html = etree.HTML(text)
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
            res4_f.append(listA)
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
    df_f = pd.DataFrame(res4_f)
    return df_f

@retry(2, 5)
async def get_cyrjg(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/cyrjg_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            if text is None:
                res4_f.append(['未获取'] * 5)
                continue
            html = etree.HTML(text)
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
            res4_f.append(listA)
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
    df_f = pd.DataFrame(res4_f)
    return df_f

@retry(2, 5)
async def get_gmbd(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/gmbd_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            if text is None:
                res4_f.append(['未获取'] * 8)
                continue
            html = etree.HTML(text)
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
            res4_f.append(listA)
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
    df_f = pd.DataFrame(res4_f)
    return df_f

@retry(2, 5)
async def get_jjjl(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/jjjl_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            if text is None:
                res4_f.append(['未获取'] * 6)
                continue
            html = etree.HTML(text)
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
            res4_f.append(listA)
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
    df_f = pd.DataFrame(res4_f)
    return df_f

@retry(2, 5)
async def get_tsdata(rrs: list):
    global la
    code_list = la['基金代码'].tolist()
    if rrs:
        code_list = code_list[rrs[0]:rrs[1]]
        # 复制并更新索引
        # la = la.iloc[rrs[0]:rrs[1]]
        # la.index = range(len(la))

    res4_f = []
    url = 'http://fundf10.eastmoney.com/tsdata_xxxxx.html'
    for i in range(len(code_list)):
        try:
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
                'dumpio': True,  # 解决浏览器多开卡死
            }
            browser = await launch(**launch_args)
            page = await browser.newPage()
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                             '{ webdriver:{ get: () => false } }) }')
            resp = await page.goto(url=url.replace('xxxxx', str(code_list[i])), timeout=60000)
            print(f"func[{sys._getframe().f_code.co_name}]的第[{i+1}]个/共{len(code_list)}个 : current code:[{code_list[i]}]")
            if resp.status != 200:
                pass
            text = await page.content()
            await browser.close()
            end_time = time()
            print(f"Request costs :{end_time - start_time:.2f}s")
            if text is None:
                res4_f.append(['未获取'] * 2)
                continue
            html = etree.HTML(text)
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
            res4_f.append(listA)
        except Exception as err_info:
            print(f"[{sys._getframe().f_code.co_name}]=>error_info:[{err_info}]")
    df_f = pd.DataFrame(res4_f)
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
    # url_list = ["http://fundf10.eastmoney.com/jdzf_000179.html", "http://fundf10.eastmoney.com/jndzf_000179.html",
    #             "http://fundf10.eastmoney.com/tsdata_000204.html", "http://fundf10.eastmoney.com/cyrjg_000179.html",
    #             "http://fundf10.eastmoney.com/gmbd_000179.html", "http://fundf10.eastmoney.com/jjjl_000179.html",
    #             ]  # , "http://www.10010.com/net5/011/", "http://python.jobbole.com/87541/"
    # tasks = [get_html(url_list[0]), get_html(url_list[1]), get_html(url_list[2]), get_html(url_list[3]), get_html(url_list[4]),get_html(url_list[5])]

    ranges = [0, 6945]
    # 10个：62s 20个：116s 100个：1335s 600个 9172s  15s/个
    # 极端： 5个 128s 20个：
    tasks = [get_jdzf(rrs=ranges), get_jndzf(rrs=ranges), get_cyrjg(rrs=ranges), get_gmbd(rrs=ranges),
             get_jjjl(rrs=ranges), get_tsdata(rrs=ranges)]

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
    results = loop.run_until_complete(
        asyncio.gather(*tasks))  # loop.run_until_complete() 既可以接收一个协程对象, 也可以接收一个 future 对象

    # # cost 35s
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[0]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[1]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[2]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[3]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[4]))
    # asyncio.get_event_loop().run_until_complete(get_html(url_list[5]))

    # loop.close()

    # 合并6组数据
    # for res in results:
    #     print(res)
    # print(results[0],results[1],results[2],results[3],results[4],results[5])
    # print(la)
    dd = la.iloc[ranges[0]:ranges[1]]
    dd.index = range(len(dd))
    # print(dd)

    # 合并数据写入funds_full_info.csv
    fal = pd.concat([dd,results[0],results[1],results[2],results[3],results[4],results[5]], axis=1)
    fal.to_csv('funds_full_info.csv', mode='a+', index=False, header=False)

    # csv 转成 xlsx 带上标题
    # to do

    print(f"全部请求完成,耗时:[{time() - s_time:.2f}s].开始于:{s_time:.2f} 结束于:{time():.2f}")
