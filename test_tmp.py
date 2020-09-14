# import threading
# # import time
# #
# #
# # def test_thread(n, a=[]):
# #     print(f"task {n}")
# #     time.sleep(1)
# #     print(f"{n} sleep 1s")
# #     time.sleep(2)
# #     print(f"{n} sleep 2s")
# #     time.sleep(3)
# #     print(f"{n} sleep 3s")
# #     print(f"list is:{a}")
# #
# #
# # if __name__ == "__main__":
# #     listA = [1, 2, 3]
# #     listB = [6, 7, 8]
# #     t1 = threading.Thread(target=test_thread, args=("t1", listA))
# #     t2 = threading.Thread(target=test_thread, args=("t2", listB))
# #
# #     t1.setDaemon(True)
# #     t1.start()
# #     t2.start()
# #
# #     # t1.setName()
# #     t1.getName()
# #
# #     t1.join(timeout=10)
# #     t2.join(timeout=10)


# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, threading, datetime
from bs4 import BeautifulSoup
import random

import requests
from fake_useragent import UserAgent

my_proxies={'http':'113.194.29.106:9999'}
my_proxies2={'http':'113.194.29.106:9999'}
my_proxies3={'http':'111.222.141.127:8118'}

list_prxy=[{},{},{}]

ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}  #

# res=requests.get(url="http://icanhazip.com",proxies=my_proxies3,timeout=7)
# res2=requests.get(url="http://icanhazip.com",proxies={'http':'113.194.29.106:9999'},headers=headers,timeout=20)
# res2=requests.get(url="http://httpbin.org/ip",proxies={'http':'113.194.29.106:9999'},timeout=20)
# res2=requests.get(url="http://api.ipify.org ",proxies={'http':'113.194.29.106:9999'},timeout=20)
res2=requests.get(url="https://www.baidu.com",proxies={'https':'171.12.115.181:9999'},timeout=20)


# print(res.text)
print(res2.status_code)

# try:
#     requests.get('http://wenshu.court.gov.cn/', proxies={"http":"125.108.99.41:9000"},timeout=7)
# except:
#     print('connect failed')
# else:
#     print('success')
