"""
Date:   2020-8-24
Author: terry.wang
topic:  for test fetch 91porn videos and download
usage:  1.提前在ini中配置好91porn最新网址和浏览器访问cookie
        2.调用链: start_by_number -> __fetch_videoUrlInfo ->__cdn_download
        -> CDNDownloader() -> merge_ts_video
"""

from time import time
import requests
import random
import logging
import re
from progressbar import *
import time
import base64
from configparser import ConfigParser
import threading
import execjs
import asyncio
from pyppeteer import launch
from lib_logger import MyLogger
import csv
from lxml import etree
from cdn_downloader import CDNDownloader
import os
from collections import defaultdict

config = ConfigParser()
config.read("urls_rules.ini")

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# logger.info(f"[{config['video_urls']['index_page']}]")
# logger.info(f"[{config['rules']['sub_page_rule']}]")
# logger.info(f"[{config['rules']['video_rule']}]")

gl_cookie = "CLIPSHARE=47348bded4f2af853474ce2a7df2d7c2; __utmc=20744104; __utmz=20744104.1630418255.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=20744104.746455921.1630418255.1632658768.1632661630.14; __utmb=20744104.0.10.1632661630; covid=0f5dt+u+C8aGzQtx1sicxRb+/OMtttxzw0HI+ZqE"


class My91DownLoad(MyLogger):
    _favo_video_url = "https://0722.91p51.com/video.php?category=rf&page=1"
    _current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    _current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self):
        """
        初始化: 创建文件夹目录+初始化日志模块
        """
        super().__init__(__name__, logging.INFO)
        self.log_dir = 'logs/' + self._current_day
        self.storage_dir = 'video/' + self._current_day
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def start_by_number(self, number: int = 0, method: int = 0):
        """
        统一开始请求+下载入口
        :param number: int 下载个数，超过每页24 自动翻页
        :param method: 方式：0-cdn ts流下载 1-request+strencode加密解密方式
        :return:
        """
        list_urls, title_cdncode_dict = self.__fetch_videoUrlInfo(number)
        if method == 0:
            self.__cdn_download(title_cdncode_dict)
        elif method == 1:
            list_videos, list_titles = self.fetch_video_urls(list_urls)
        else:
            self.logger.info(f"Unknown method.check args:method value")
        # 可以考虑使用多线程下载
        # threads=5
        # for i in range(threads):
        #     t = threading.Thread(target=self.download_videos, args=(list_videos,list_titles))
        #     t.start()
        # for in range(threads):
        #     t.join()
        self.logger.info(f"list_titles and list_videos : [{list_titles}]\n [{list_videos}]")
        self.download_videos(title_lists=list_titles, video_lists=list_videos)

    def __fetch_videoUrlInfo(self, number: int = 0):
        """
        主入口:index页面获取每个视频相关的url,cdn编号等信息
        number: 获取个数
        :return:
        """
        pages = number // 24 + 1

        url_list = []
        title_cdn_dict = {}
        title_cdn_dict_final = {}
        for page in range(pages):
            current_url = config['index']['index_page'].replace("page=xxx", f"page={page + 1}")
            self.logger.info(f"__fetch_videoUrlInfo 请求url : {current_url}\n")
            headers = {
                'User-Agent': config['UA']['user_agent'],
                'Referer': current_url,
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                # 'cookie': config['COOKIE']['value']
                'cookie': gl_cookie
            }
            res1 = requests.request('GET', current_url, headers=headers)
            # self.logger.info(f"res1.status_code : {res1.status_code}")
            # self.logger.info(f"res1.text include: {res1.text}")
            print(res1.text)

            subpage_re_rules = [
                'https://a1016.91p01.com/view_video.php\\?viewkey=.*&page=.*&viewtype=.*&category=.{2}',  # 子url
                '<img class="img-responsive" src="https://i.91p22.net/thumb/(.*?).jpg"/>',  # cdn编号
                '<span class="video-title title-truncate m-t-5">(.*?)</span>'  # title名字
            ]

            url_list_page = re.findall(subpage_re_rules[0], res1.text)
            cdn_code_page = re.findall('<img class="img-responsive" src="https://i.91p22.net/thumb/(.*?).jpg"',
                                       res1.text)
            title_page = re.findall('<span class="video-title title-truncate m-t-5">(.*?)</span>', res1.text)

            # 格式化title名字
            for i in range(len(title_page)):
                title_page[i] = title_page[i].replace(' ', '')
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                title_page[i] = re.sub(rstr, "_", title_page[i])  # 替换为下划线

            url_list_set = list(set(url_list_page))
            for i in range(len(url_list_set)):
                url_list.append(url_list_set[i])

            for i in range(len(cdn_code_page)):
                title_cdn_dict[title_page[i]] = cdn_code_page[i]

        if 0 < number:
            url_list = url_list[0:number]
            count_tmp = 0
            for k, v in title_cdn_dict.items():
                if count_tmp < number:
                    title_cdn_dict_final[k] = v
                    count_tmp += 1

        self.logger.info(f"fetch_subpage_urls-请求:[{number}]个. 实际获得url : [{len(url_list)}]个")
        self.logger.info(f"fetch_subpage_urls-请求:[{number}]个. 实际获得title+cdn_code: [{len(title_cdn_dict_final)}]对")
        self.logger.info(f"title_cdn_dict 是: {title_cdn_dict_final}")
        return url_list, title_cdn_dict_final

    def __cdn_download(self, title_cdn_dict: dict):
        """
        通过cdn编码进行下载ts码流集合的下载和封面图片的下载，然后合并ts码流文件
        :type title_cdn_dict: object
        :return:
        """
        img_url = 'https://i.91p22.net/thumb/xxx.jpg'
        start_time = time.time()
        for k, v in title_cdn_dict.items():
            save_path = self.storage_dir + '/' + k
            self.logger.info(f"save_path: {save_path}")
            # 已经存在对应的目录就不在进行ts爬取下载
            if os.path.exists(save_path):
                continue
            # 下载ts片段
            t = CDNDownloader(v, save_path)
            t.start()
            # 必须阻塞执行
            t.join()
            # 下载封面图
            res_img = requests.get(img_url.replace('xxx', v))
            if res_img.ok is True:
                with open(save_path + k + '.jpg', 'w') as ff:
                    ff.write(res_img.content)

            # 下载完成后合并所有ts文件为mp4
            # 删除*.ts
            self.merge_ts_video(source_path=save_path, target_path=save_path, file_name=k)

        self.logger.info(f"下载一共用时: {time.time() - start_time}.2f 秒")
        self.logger.info("当前所有下载完成，请检查.")

    def merge_ts_video(self, source_path, target_path, file_name: str):
        """
        合并文件
        :param source_path: 源路径
        :param target_path: 目标路径
        :param file_name:  保存文件名
        :return:
        """
        all_ts = os.listdir(source_path)
        merge_file_name = target_path + '/' + file_name
        # self.logger.info(merge_file_name)
        with open(merge_file_name, 'wb+') as f:
            for i in range(len(all_ts)):
                ts_video_path = os.path.join(source_path, all_ts[i])
                f.write(open(ts_video_path, 'rb').read())

        if os.path.exists(merge_file_name):
            shell_str1 = 'del ' + source_path + '\\' + '*.ts'
            os_res = os.system(shell_str1)
            if os_res == 0:
                self.logger.info(f"[{merge_file_name}]merge完成,删除*.ts文件完成")
            return True
        else:
            return False

    def fetch_video_urls(self, listA: list, retry_times: int = 0):
        """
        详情页入口:获取所有子详情页对应的各种类型下载urls
        :param listA:
        :return:返回存储了video title img的lists
        @param listA: 存储子详情页urls链接的列表
        @param retry_times: 重试次数
        """
        self.logger.info(f"start request subpages:get video urls.")
        video_lists = []
        title_lists = []
        for i in range(len(listA)):
            self.logger.info(f"\n")
            self.logger.info(f"开始请求第[{i + 1}]个subpage===>")
            #  获取等video url 404: 需要解决这里的 cookies等加上获取等内容 == request获取内容
            # referer need user subpage url
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': config['UA']['user_agent'],
                'referer': listA[i],
                'Content-Type': 'multipart/form-data; session_language=cn_CN',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                # 'cookie': config['COOKIE']['value']
                'cookie': gl_cookie
            }

            res2 = requests.request('GET', listA[i], headers=headers)
            if res2.status_code != 200:
                self.logger.info(f"subpage url:[{listA[i]}] retrun an Error: status_code:[{res2.status_code}]")
                with open(self._current_day + '_request_subpage_failed.log', 'w', encoding='utf-8') as f:
                    f.write(f"\n请求失败的subpage_url:[{listA[i]}]\n\n")
            else:
                self.logger.info(f"subpage url:[{listA[i]}],status_code: [{res2.status_code}]")
                pass

            # fecth video
            viode_re_rules = [
                'http.?://.*.91p\d{2}.com/.?mp43/.*.mp4\\?.*=.*&f=[^"]*',
                'http.?://.*.91p48.com//mp43/.*.mp4\\?secure=.*&f=[^"]*'
            ]
            url_re = re.findall(viode_re_rules[0], str(res2.text))
            # url_re = re.findall(config['index']['video_rule'], str(res2.text))
            url_re = list(set(url_re))

            if url_re:
                video_url = url_re[0]
                self.logger.info(f"第{i + 1}个re video url:[{video_url}]")
                video_lists.append(video_url)

            else:
                self.logger.info(f"re video url failed.try use strencode method.")
                '''如果正常匹配条件没匹配到对应的视频url,则尝试匹配strencode函数解析对应视频url'''
                strencode = re.findall(r'document.write\(strencode\("(.*)"', str(res2.text))
                if not strencode:
                    self.logger.info(
                        f"第{i + 1}个url:re and strencode() both failed.more details see error log:{self._current_day + '_parse_video_url_error.log'}")
                    with open(self.log_dir + "/" + self._current_day + '_error.log', "a", encoding='utf-8') as f:
                        f.write(f"\n请求时间:[{self._current_time}]\n")
                        f.write(f"正则匹配和strencode都失败subpage_url:[{listA[i]}]\n")
                        f.write(res2.text)
                        f.write("===============================================================================\n")
                    continue
                else:
                    # re match failed,but get strencode()
                    self.logger.info(f"第{i + 1}个url:strencode() rematch success.")
                    self.logger.info(f"strencode args:{strencode}")
                    temp = strencode[0].split(',')
                    input = temp[0].replace('"', '')
                    encode_key = temp[1].replace('"', '')
                    video_url_strencode = self.strdecode(input=input, key=encode_key)
                    self.logger.info(f"第{i + 1}个strencode解析出来的video_url:[{video_url_strencode}]")
                    video_lists.append(video_url_strencode)

                # fetch title
                html = etree.HTML(res2.text)
                tittle_tmp = html.xpath('//*[@id="videodetails"]/h4/text()')
                temp_t = tittle_tmp[0].replace('\n', '')
                tittle_f = temp_t.replace(' ', '')
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                tittle_f = re.sub(rstr, "_", tittle_f)  # 替换为下划线
                self.logger.info(f"获取到的tiltle是:[{tittle_f}]")
                title_lists.append(tittle_f)

            time.sleep(3)

        self.logger.info(f"共请求{len(listA)}个,成功请求[{len(video_lists)}]个...")
        # 保存video url到 csv文件
        save_file_name = self.log_dir + '/' + self._current_day + '_video_lists.csv'
        with open(save_file_name, 'a+', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(['标题title', '视频链接video_url'])
        with open(save_file_name, "a+", encoding='utf-8-sig') as f:
            tmp_list = [title_lists, video_lists];
            writer = csv.writer(f, dialect='excel')
            writer.writerow(tmp_list)
        self.logger.info(f"已保存title+video信息到文件到当日csv...")

        return video_lists, title_lists

    def download_videos(self, video_lists: list, title_lists: list):
        """
        下载所有video
        :param video_lists:存储了视频下载urls的列表
        :param title_lists:存储了对应的标题 名字的列表
        :return:
        """
        assert video_lists, "video_lists为空, 请检查"
        assert title_lists, "title_lists为空，请检查"
        # 检查文件夹
        current_day_dir = self.storage_dir
        if not os.path.exists(current_day_dir):
            os.mkdir(current_day_dir)
        else:
            pass

        self.logger.info(f"共[{len(video_lists)}]个视频,开始下载======")
        for i in range(len(video_lists)):
            video_name = title_lists[i] + '.mp4'
            headers = {
                'User-Agent': config['UA']['user_agent'],
                'Referer': config['index']['index_page'].replace("page=xxx", "page=1"),
                # 'cookie': config['COOKIE']['value']
                'cookie': gl_cookie
            }
            self.logger.info(f"共[{len(video_lists)}]个/第[{i + 1}]个\n[{title_lists[i]}]\n[{video_lists[i]}]\n")
            try:
                res3 = requests.request('GET', url=video_lists[i], headers=headers, timeout=300)
                total_length = int(res3.headers.get("Content-Length"))
                self.logger.info(f"文件大小:[{total_length // (1024 * 1024)}]M.")
            except Exception as error_info:
                self.logger.info(f"第[{i + 1}]个video请求失败:[{error_info}].将跳过...\n")
                continue
            if res3.status_code != 200:
                self.logger.info(f"第[{i + 1}]个video请求失败, status_code:[{res3.status_code}]")
                continue
            else:
                pass

            if os.path.exists(current_day_dir + '/' + video_name):
                self.logger.info(f"video:[{video_name}]在目录:[{current_day_dir}]已存在.跳过...\n")
                continue
            else:
                self.logger.info(f"开始下载...")
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
                self.logger.info(f"下载成功...\n")
            time.sleep(3)
        self.logger.info(f"[wonderful!!!]所有下载任务请求完成,请检查...")

    def proxy_set(self):
        """
        设置代理访问,to do
        :return:
        """
        pass

    @staticmethod
    def strdecode(input, key):
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

    def __js_exec(self, strencode: list):
        """
        调用js解密：pyexcejs库功能 node.js/phantomjs...
        :param strencode: 实际解密参数
        :return:
        """
        print(f"run environ: {execjs.get().name}")
        ctx = execjs.compile(open(r"strencode.js").read())
        ctx.call("strencode", strencode[0], strencode[1])

    async def __pyppeteeer_newget(self, subpage_url):
        # self.logger.info(f"开始请求video_url")
        start = time.time()
        timeout = 180
        # 具体用法参考:  https://www.cnblogs.com/trojan-z/p/12072211.html
        launch_args = {
            "headless": True,  # 关闭无头浏览器
            'devtools': False,  # 控制界面的显示，用来调试
            "args": [
                "--start-maximized",
                "--no-sandbox",  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                "--disable-infobars",
                "--ignore-certificate-errors",
                "--log-level=3",
                "--enable-extensions",
                "--window-size=1920,1080",
                f"\"--refer={self._favo_video_url}\"",
                f"\"--user-agent={config['UA']['user_agent']}\"",
            ],
            'dumpio': True,  # 解决浏览器多开卡死
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        # COOKIES 手动改
        # cookies = {'domain': subpage_url, 'CLIPSHARE': '47348bded4f2af853474ce2a7df2d7c2', '__utmc': '20744104',
        #            '__utmz': '20744104.1630418255.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        #            '__utma': '20744104.746455921.1630418255.1632040468.1632208017.6',
        #            '__utmb': '20744104.0.10.1632208017',
        #            'covid191': '6eb5si1Z7T+g1vQvFnkRLcG7C5GO9V/uoO3Q+5IC'}
        #
        # for item in cookies:
        #     await page.setCookie(item)
        await page.setExtraHTTPHeaders({'Cookie': gl_cookie})
        # 'https://0722.91p51.com/view_video.php?viewkey=5f1ce5096ebc088204d5&page=1&viewtype=basic&category=rf',timeout=60000)
        res = await page.goto(subpage_url, options={'timeout': timeout * 1000})  # 跳转
        # await page.screenshot({'path': 'example.png'})  # 截图
        # page.title() res.status res.headers

        # get video download links
        viode_re_rules = [
            '(http.?://.*.91p\d{2}.com/.?mp43/.*.mp4\\?.*=.*f=[^"]*)',
        ]
        with open("tmp.html", "w", encoding='utf-8') as f:
            f.write(str(await page.content()))
        video_ori = re.findall(viode_re_rules[0], str(await page.content()))
        self.logger.info(str(await page.content()))
        video_ori = list(set(video_ori))
        self.logger.debug(f"video_ori is:{video_ori}\n")
        # with open(self._current_day+"context"+".log",'a') as f:
        #     f.write(await page.content())

        if not video_ori:
            self.logger.info(f"__pyppeteeer_newget-报错:没有匹配到任何video_url,将直接return.")
            await browser.close()
            return None
        else:  # 特殊处理
            if len(video_ori) > 1:
                video_f = min((word for word in video_ori if word), key=len)
            else:
                video_f = video_ori[0]
            self.logger.info(f"\n获取到的video_url是:{video_f}\n")

        await browser.close()  # 关闭
        end = time.time()
        self.logger.info(f"请求花费时间:[{end - start}]")
        return video_f

    def fetch_video_pypt(self, listB: list):
        """
        获取所有下载链接新接口:使用chrome的puppeteer py版本库:pyppeteer.
        模拟无头浏览器环境 获取js动态渲染内容,曲线解密strencode+m.js
        :param listB: 存储子详情页urls链接的列表
        :return:返回存储了video title img的lists
        """
        self.logger.info(f"fetch_video_urls_new : 开始请求video_url...\n")
        # 保存video_url到csv文件
        save_file_name = self.log_dir + '/' + self._current_day + '_video_lists.csv'
        with open(save_file_name, 'a+', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(['标题title', '视频链接video_url'])
        video_lists = []
        title_lists = []
        for i in range(len(listB)):
            try:
                self.logger.info(f"第[{i + 1}]个subpage_url:[{listB[i]}]")
                headers = {
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'User-Agent': config['UA']['user_agent'],
                    'referer': listB[i],
                    'Content-Type': 'multipart/form-data; session_language=cn_CN',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    # 'cookie': config['COOKIE']['value']
                    'cookie': gl_cookie
                }
                res2 = requests.request('GET', listB[i], headers=headers)
                if res2.status_code != 200:
                    self.logger.info(f"本次请求异常,status_code:[{res2.status_code}].将跳过...")
                    with open(self._current_day + '_request_subpage_failed.log', 'w', encoding='utf-8') as f:
                        f.write(f"\n请求失败subpage_url:\n[{listB[i]}]\n")
                    continue
                else:
                    pass

                html = etree.HTML(res2.text)
                tittle_tmp = html.xpath('//*[@id="videodetails"]/h4/text()')  # //*[@id="videodetails"]/h4
                # //*[@id="wrapper"]/div[1]/div[3]/div/div/div[1]/div/a
                # //*[@id="wrapper"]/div[1]/div[3]/div/div/div[2]/div/a
                # //*[@id="wrapper"]/div[1]/div[3]/div/div/div[3]/div/a
                temp_t = tittle_tmp[0].replace('\n', '')
                tittle_f = temp_t.replace(' ', '')
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                tittle_f = re.sub(rstr, "_", tittle_f)  # 替换为下划线
                self.logger.info(f"获取到的tiltle是:[{tittle_f}]")

                # 获取video下载url
                video_f = asyncio.get_event_loop().run_until_complete(self.__pyppeteeer_newget(subpage_url=listB[i]))

                if not (video_f or tittle_f):  # or img_f:
                    self.logger.info(f"本次subpage解析(video,title)有数据不存在,退出第[{i + 1}]次循环")
                    continue
                else:
                    video_lists.append(video_f)
                    title_lists.append(tittle_f)

                    with open(save_file_name, "a+", encoding='utf-8-sig') as f:
                        tmp_list = [tittle_f, video_f];
                        writer = csv.writer(f, dialect='excel')
                        writer.writerow(tmp_list)
                    self.logger.info(f"已保存title+video信息到文件到当日csv...")

            except TypeError as error_info:
                self.logger.info(f"捕获异常-error_info:[{error_info}],将跳过此次请求 ")
                continue

        time.sleep(3)
        self.logger.info(f"共请求{len(listB)}个,成功请求[{len(video_lists)}]个...")

        return video_lists, title_lists


if __name__ == '__main__':
    f = My91DownLoad()
    # 最大number=25,单页24个 [作为游客，你每天只可观看25个视频]
    f.start_by_number(number=1, method=0)

    """
    @staticmethod
    def strdecode(input, key):
    """
    # url = f.strdecode(
    #     "%3c%73%6f%75%72%63%65%20%73%72%63%3d%27%68%74%74%70%73%3a%2f%2f%63%64%6e%2e%39%31%70%30%37%2e%63%6f%6d%2f%2f%6d%33%75%38%2f%35%32%36%32%39%38%2f%35%32%36%32%39%38%2e%6d%33%75%38%3f%73%74%3d%62%59%75%62%79%4f%45%30%6d%6d%31%4c%69%77%37%54%36%72%41%4b%4f%67%26%65%3d%31%36%33%32%32%31%38%39%30%34%27%20%74%79%70%65%3d%27%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%2d%6d%70%65%67%55%52%4c%27%3e")
    # print(url)
