"""
Date:2020-8-24
Author:terry.wang
topic:for test fetch videos and store in my folders 91pprn
usage: url获取有两种方式 1.video url直接re  2. strencode加密解密获取
"""

import datetime
from time import time
import requests
import os
import random
import logging
import re
from progressbar import *
import time
import base64
from fake_useragent import UserAgent
from configparser import ConfigParser
import threading
import execjs
import asyncio
from pyppeteer import launch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = ConfigParser()
config.read("urls_rules.ini")

logger.info(f"[{config['urls']['index_page']}]")
logger.info(f"[{config['rules']['sub_page_rule']}]")
logger.info(f"[{config['rules']['video_rule']}]")


class My91DownLoad():
    _favo_video_url = "https://0722.91p51.com/video.php?category=rf&page=1"
    _current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    _current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self):
        self.log_dir = 'logs/' + self._current_day
        self.storage_dir = 'video/' + self._current_day
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def start(self, number: int = 0):
        """
        统一开始请求+下载入口
        :type number: int 下载个数，超过每页24 自动翻页
        :return:
        """
        list_urls = self.fetch_subpage_urls(number)

        # list_videos, list_titles, list_images = self.fetch_video_urls(list_urls)
        list_videos, list_titles, list_images = self.fetch_video_urls_new(list_urls)

        # 可以考虑使用多线程下载
        # threads=5
        # for i in range(threads):
        #     t = threading.Thread(target=self.download_videos, args=(list_videos,list_titles))
        #     t.start()
        # for in range(threads):
        #     t.join()
        self.download_videos(title_lists=list_titles, video_lists=list_videos)

    def fetch_subpage_urls(self, number: int = 0):
        """
        主入口:index页面去取得子详情页url
        number: 爬去subpage个数,每页最多24个。超过需翻页(未实现).默认:0-仅下载当前页24个
        :return:
        """
        pages = number // 24 + 1

        url_list = []
        ua = UserAgent()
        for page in range(pages):
            current_url = config['urls']['index_page'].replace("page=1", f"page={page + 1}")
            # current_url = self._favo_video_url.replace("page=1", f"page={page + 1}")
            logger.info(f"start request index url : {current_url}")
            headers = {
                'User-Agent': ua.random,
                'Referer': current_url,
            }
            res1 = requests.request('GET', current_url, headers=headers)
            logger.debug(f"res1.status_code : {res1.status_code}")
            logger.debug(f"res1.text include: {res1.text}")

            logger.info(f"start parse: get subpage urls:")
            subpage_re_rules = [
                'https://0722.91p51.com/view_video.php\\?viewkey=.*&page=.*&viewtype=.*&category=.{2}',
                'temp'
            ]
            url_list_page = re.findall(subpage_re_rules[0], res1.text)
            # url_list_page = re.findall(config['rules']['sub_page_rule'],res1.text)
            url_list_set = list(set(url_list_page))
            for i in range(len(url_list_set)):
                url_list.append(url_list_set[i])

        if 0 < number:
            url_list = url_list[0:number]
            logger.debug(f"url_list[0:1] is: {url_list[0:1]}")
            logger.info(f"请求number:[{number}]个. 实际存储数量: {len(url_list)}")

        return url_list
        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(1) > div > a
        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(2) > div > a
        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(3) > div > a
        # // *[ @ id = "wrapper"] / div[1] / div[2] / div / div / div[1] / div / a
        # / html / body / div[4] / div[1] / div[2] / div / div / div[1] / div / a

    def fetch_video_urls(self, listA: list, retry_times: int = 0):
        """
        详情页入口:获取所有子详情页对应的各种类型下载urls
        :param listA: 存储子详情页urls链接的列表
        :return:返回存储了video title img的lists
        """
        logger.info(f"start request subpages:get video urls.")
        video_lists = []
        title_lists = []
        image_lists = []
        for i in range(len(listA)):
            logger.info(f"\n")
            logger.info(f"开始请求第[{i+1}]个subpage===>")
            ua = UserAgent()
            #  获取等video url 404: 需要解决这里的 cookies等加上获取等内容 == request获取内容
            # referer need user subpage url
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': ua.random,
                'referer': listA[i],
                'Content-Type': 'multipart/form-data; session_language=cn_CN',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            res2 = requests.request('GET', listA[i], headers=headers)
            if res2.status_code != 200:
                logger.info(f"subpage url:[{listA[i]}] retrun an Error: status_code:[{res2.status_code}]")
                with open(self._current_day + '_request_subpage_failed.log', 'w', encoding='utf-8') as f:
                    f.write(f"\n请求失败的subpage_url:[{listA[i]}]\n\n")
            else:
                logger.info(f"subpage url:[{listA[i]}],status_code: [{res2.status_code}]")
                pass

            # with open(self.log_dir+'/'+self._current_day+'_debug.log','a',encoding='utf-8') as f:
            #     f.write("\n\n\n\n\n\n\n\n\n\n\n"+res2.text)
            #     f.write("=====================================================================================\n\n\n\n\n\n")

            '''
            need match url:
            https://cfdc.91p52.com//mp43/394884.mp4?st=7g3X27wzvJ7trgWsrD04bw&f=21721FpSf29IlSEb1YBEyXegQozQ/0IPjvl7vGtDcx/0ljKiZNttL3wXA6rpuzFY81JgyEK3GFC3Ig7KNcBKFbHKNCi14clux519OA
            http://ccn.91p52.com//mp43/394860.mp4?st=R6_UOfDg2oetpIKj-ALfGw&f=deaakSKNEsavSOcP5BiYu05HKa5+t5KvygkmIQTso6/XsDrgsX0HUtOaUvRsaYQvYuWoYCEv3UHhxsPi6o6RP2rCfhqVM9asxzgfhA
            http://v2.91p48.com/mp43/394859.mp4?secure=qIlFsnni3ERBZn52NxRK6w==,1599661756&f=b7dbK/zaJ8gdvNiYWVv/J+qZmLqhem3UeY3xjwuPAvPjQwedTjlW+zrtInhUwFEOUY5WIBYkRZORX/OTCDmartj1XFHkDlRSeTD/VlARECVpzh5eeOX/l6svuQc
            '''
            # fecth video
            viode_re_rules = [
                'http.?://.*.91p\d{2}.com/.?mp43/.*.mp4\\?.*=.*&f=[^"]*',
                'http.?://.*.91p48.com//mp43/.*.mp4\\?secure=.*&f=[^"]*'
            ]
            url_re = re.findall(viode_re_rules[0], str(res2.text))
            # url_re = re.findall(config['rules']['video_rule'], str(res2.text))
            url_re = list(set(url_re))

            if url_re:
                video_url = url_re[0]
                logger.info(f"第{i+1}个re video url:[{video_url}]")
                video_lists.append(video_url)

            else:
                logger.info(f"re video url failed.try use strencode method.")
                '''如果正常匹配条件没匹配到对应的视频url,则尝试匹配strencode函数解析对应视频url'''
                strencode = re.findall(r'document.write\(strencode\("(.*)"', str(res2.text))
                if not strencode:
                    logger.info(f"第{i+1}个url:re and strencode() both failed.more details see error log:{self._current_day + '_parse_video_url_error.log'}")
                    with open(self.log_dir + "/" + self._current_day + '_error.log', "a", encoding='utf-8') as f:
                        f.write(f"\n请求时间:[{self._current_time}]\n")
                        f.write(f"正则匹配和strencode都失败subpage_url:[{listA[i]}]\n")
                        f.write(res2.text)
                        f.write("===============================================================================\n")
                    continue
                else:
                    # re match failed,but get strencode()
                    logger.info(f"第{i+1}个url:strencode() rematch success.")
                    logger.info(f"strencode args:{strencode}")
                    temp = strencode[0].split(',')
                    input = temp[0].replace('"', '')
                    encode_key = temp[1].replace('"', '')
                    video_url_strencode = self.__strdecode(input=input, key=encode_key)
                    logger.info(f"第{i+1}个strencode video_url is:[{video_url_strencode}]")
                    video_lists.append(video_url_strencode)

                # fetch title
                tittle = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>', res2.text, re.S)
                temp_t = tittle[0].replace('\n', '')
                tittle_f = temp_t.replace(' ', '')
                logger.info(f"tiltle is:{tittle_f}")
                # fetch img
                img_url = re.findall(r'poster="(.*?)"', str(res2.text))
                logger.debug(f"img_url is:{img_url}")
                image_lists.append(img_url)
                title_lists.append(tittle_f)

            time.sleep(3)

        logger.info(f"共请求{len(listA)}个,成功请求[{len(video_lists)}]个...")
        with open(self.log_dir + '/' + self._current_day + '_video_lists.log', "w") as f:
            f.write(self._current_time + ':\n')
            for v in range(len(video_lists)):
                f.write(title_lists[v] + "\n" + video_lists[v] + "\n")

        # if retry_times == 0:
        #     pass
        # else:
        #     for r in range(retry_times):
        #         logger.info(f"开始第[{r + 1}]次重试")

        return video_lists, title_lists, image_lists

    def download_videos(self, video_lists: list, title_lists: list):
        """
        下载所有video
        :param video_lists:存储了视频下载urls的列表
        :param title_lists:存储了对应的标题名字的列表
        :return:
        """
        assert video_lists, "video_lists为空,无需下载"
        assert title_lists, "title_lists为空，请检查"
        # 检查文件夹
        current_day_dir = self.storage_dir
        if not os.path.exists(current_day_dir):
            os.mkdir(current_day_dir)
        else:
            pass

        for i in range(len(video_lists)):
            video_name = title_lists[i] + '.mp4'
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random,
                # 'Host': 'cfdc.91p52.com',
                # 'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
                # 'Accept - Encoding': 'gzip, deflate, br',
                # 'Accept - Language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
                # 'Cache - Control': 'max - age = 0',
                # 'Connection': 'keep-alive',
                # 'Range': 'bytes=0-16092',
                # 'Sec-Fetch-Dest': 'document',
                # 'Sec-Fetch-Mode': 'navigate',
                # 'Sec-Fetch-Site': 'none',
                # 'Sec-Fetch-User': '?1',
                # 'Upgrade - Insecure - Requests': '1',
                'Referer': self._favo_video_url,
                # 'cookie':'',
            }  # Referer？ video url不正确  #看一下对应的链接 请求头
            logger.info(f"共[{len(video_lists)}]个视频,开始下载第[{i+1}]个======>")
            logger.info(f"第[{i+1}]个[{title_lists[i]}]:[{video_lists[i]}]\n")
            res3 = requests.request('GET', url=video_lists[i], headers=headers)
            total_length = int(res3.headers.get("Content-Length"))
            logger.info(f"该文件大小:[{total_length // (1024 * 1024)}]M.")
            if res3.status_code != 200:
                logger.info(f"video download failed:[{video_lists[i]}] status_code:[{res3.status_code}]")
                continue
            else:
                pass

            if os.path.exists(current_day_dir+'/'+video_name):
                logger.info(f"video file: [{video_name}] already exist in [{current_day_dir}].will continue~\n")
                continue
            else:
                logger.info(f"start download.")
                with open(current_day_dir + '/' + video_name, "wb") as f:
                    widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                               FileTransferSpeed()]
                    down_progress = ProgressBar(widgets=widgets, maxval=total_length)
                    down_progress.start()
                    dl = 0
                    for chunk in res3.iter_content(chunk_size=128):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            dl += len(chunk)
                        down_progress.update(dl)
                    down_progress.finish()
                logger.info(f"download success.\n")
            time.sleep(5)
        logger.info(f"all url in video_lists downloand success!!!wonderful!!!")

    def proxy_set(self):
        """
        设置代理访问,to do
        :return:
        """
        pass

    def __strdecode(self, input, key):
        """
        页面JS函数strencode()的解密函数
        :param input: strencode第一个参数
        :param key: strencode第二个参数
        :return:
        """
        input = base64.b64decode(input).decode("utf-8")
        str_len = len(key)
        code = ''
        for i in range(0, str_len):
            k = i % str_len
            input_i_unicode = ord(input[i])
            key_k_unicode = ord(key[k])
            code += chr(input_i_unicode ^ key_k_unicode)
        missing_padding = 4 - len(code) % 4
        if missing_padding:
            code = code + '=' * missing_padding
        code = base64.b64decode(code).decode("utf-8")
        pattern = re.compile("'(.*)' type")
        code = pattern.findall(code)
        return code[0]

    def __random_ip(self):
        """
        生成随机ip
        :return:
        """
        a = str(random.randint(1, 255))
        b = str(random.randint(1, 255))
        c = str(random.randint(1, 255))
        d = str(random.randint(1, 255))
        random_ip = a + '.' + b + '.' + c + '.' + d

        return random_ip

    def __js_exec(self,strencode:list):
        """
        调用js解密：pyexcejs库功能 node.js/phantomjs...
        :param strencode: 实际解密参数
        :return:
        """
        print(f"run environ: {execjs.get().name}")
        ctx = execjs.compile(open(r"strencode.js").read())
        ctx.call("strencode",strencode[0],strencode[1])

    async def __pyppeteeer_newget(self,subpage_url):
        logger.info(f"开始请求video_url")
        start = time.time()
        ua=UserAgent()
        timeout=360
        launch_args = {
            "headless": True,  # 关闭无头浏览器
            "args": [
                "--start-maximized",
                "--no-sandbox",
                "--disable-infobars",
                "--ignore-certificate-errors",
                "--log-level=3",
                "--enable-extensions",
                "--window-size=1920,1080",
                f"\"--refer={self._favo_video_url}\"",
                f"\"--user-agent={ua.random}\"",
            ],
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        # 'https://0722.91p51.com/view_video.php?viewkey=5f1ce5096ebc088204d5&page=1&viewtype=basic&category=rf',timeout=60000)
        res = await page.goto(subpage_url, options={'timeout': timeout*1000})  # 跳转
        # await page.screenshot({'path': 'example.png'})  # 截图

        # fecth video
        viode_re_rules = [
            '(http.?://.*.91p\d{2}.com/.?mp43/.*.mp4\\?.*=.*f=[^"]*)',
        ]
        video_ori = re.findall(viode_re_rules[0], str(await page.content()))
        video_ori = list(set(video_ori))
        logger.debug(f"video_ori is:{video_ori}\n")
        # with open(self._current_day+"context"+".log",'a') as f:
        #     f.write(await page.content())

        if not video_ori:
            logger.info(f"Error:__pyppeteeer_newget return~")
            return None
        else:
            if len(video_ori) > 1:
                video_f=min((word for word in video_ori if word), key=len)
            else:
                video_f=video_ori[0]
            logger.info(f"\nvideo_f is:{video_f}\n")

        await browser.close()  # 关闭
        end = time.time()
        print(f"total run seconds: [{end-start}]")
        return video_f


    def fetch_video_urls_new(self,listB:list):
        """
        获取所有下载链接新接口:使用chrome的puppeteer py版本库:pyppeteer.
        模拟无头浏览器环境 获取js动态渲染内容,曲线解密strencode+m.js
        :param listB: 存储子详情页urls链接的列表
        :return:返回存储了video title img的lists
        """
        logger.info(f"fetch_video_urls_new:start request subpages:get video urls.")
        video_lists = []
        title_lists = []
        image_lists = []
        for i in range(len(listB)):
            logger.info(f"\n")
            logger.info(f"开始请求第[{i+1}]个subpage===>")
            ua = UserAgent() # ua.random
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': ua.random,
                'referer': listB[i],
                'Content-Type': 'multipart/form-data; session_language=cn_CN',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            res2 = requests.request('GET', listB[i], headers=headers)
            if res2.status_code != 200:
                logger.info(f"subpage url:[{listB[i]}] retrun an Error: status_code:[{res2.status_code}]")
                with open(self._current_day + '_request_subpage_failed.log', 'w', encoding='utf-8') as f:
                    f.write(f"\n请求失败的subpage_url:[{listB[i]}]\n\n")
            else:
                logger.info(f"subpage url:[{listB[i]}],status_code: [{res2.status_code}]")
                pass
            # fetch title
            tittle = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>', res2.text, re.S)
            temp_t = tittle[0].replace('\n', '')
            tittle_f = temp_t.replace(' ', '')
            logger.info(f"tiltle is:{tittle_f}")
            # fetch img
            img_url = re.findall(r'poster="(.*?)"', str(res2.text))
            img_f=img_url[0]
            # with open("xxx.log",'a',encoding='UTF-8') as f:
            #     f.write(res2.text)
            logger.debug(f"img_url is:{img_f}")
            # fetch video
            time.sleep(5)
            video_f=asyncio.get_event_loop().run_until_complete(self.__pyppeteeer_newget(subpage_url=listB[i]))

            if not (video_f or tittle_f): #or img_f:
                logger.info(f"本次subpage解析(video,title)有数据不存在,退出第[{i+1}]次循环")
                continue
            else:
                video_lists.append(video_f)
                title_lists.append(tittle_f)
                image_lists.append(img_f)

        time.sleep(3)


        logger.info(f"共请求{len(listB)}个,成功请求[{len(video_lists)}]个...")
        with open(self.log_dir + '/' + self._current_day + '_video_lists.log', "w") as f:
            f.write(self._current_time + ':\n')
            for v in range(len(video_lists)):
                f.write(title_lists[v] + "\n" + video_lists[v] + "\n")

        # if retry_times == 0:
        #     pass
        # else:
        #     for r in range(retry_times):
        #         logger.info(f"开始第[{r + 1}]次重试")

        return video_lists, title_lists, image_lists



if __name__ == '__main__':
    f = My91DownLoad()
    #最大number=25 [作为游客，你每天只可观看25个视频]
    f.start(number=20)
