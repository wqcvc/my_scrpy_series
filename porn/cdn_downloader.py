# -*- coding: utf-8 -*-
"""
File    : cdn_downloader.py
Desc    : 通过cdn下载ts码流
Author  : terry.wang
E-mail  : 273334956@qq.com
Date    : 2021/9/25 21:57
"""

import requests
import threading
import os


class CDNDownloader(threading.Thread):
    def __init__(self, cdn_code, save_path):
        super(CDNDownloader, self).__init__()  # 继承父类的__init__函数
        self.base_url = "https://cdn.91p07.com//m3u8/"
        self.cdn_code = cdn_code
        self.save_path = save_path

    @staticmethod
    def mkdir(path):
        path = path.strip()
        path = path.rstrip("\\")
        res = os.path.exists(path)
        if not res:
            os.makedirs(path)
            return True
        else:
            return False

    def run(self):
        fragment = 0
        while True:
            url = self.base_url + self.cdn_code + "//" + self.cdn_code + str(fragment) + ".ts"
            try:
                r = requests.get(url, timeout=60)
            except requests.exceptions.RequestException as e:
                print(f"exception is: [{e}]")
            print(f"request url:[{url}],request_status: [{r.ok}]")
            if r.ok is True:
                ts_src = self.save_path + self.cdn_code
                self.mkdir(ts_src)
                with open(ts_src + "//" + str(fragment).rjust(10, '0') + ".ts", 'wb') as f:
                    f.write(r.content)
                fragment = fragment + 1
            else:
                break
        # 合并ts文件


# 运行程序
if __name__ == '__main__':

    # number 6位整数，后三位可以修改，50为一次下多少部片。
    # client_src:下载后保存在本地什么位置。
    number = 529018
    number_end = number + 10
    client_src = "D://资源//"

    while True:

        t = CDNDownloader(str(number), client_src)
        t.start()
        number = number + 1
        if number == number_end:
            break
