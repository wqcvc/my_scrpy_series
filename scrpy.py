"""
Date:2020-8-24
Author:terry.wang
topic:for test fetch videos and store in my folders
usage: to be continue
"""

import datetime
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


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config=ConfigParser()
config.read("urls_rules.ini")

logger.info(f"[{config['urls']['index_page']}]")
logger.info(f"[{config['rules']['sub_page_rule']}]")
logger.info(f"[{config['rules']['video_rule']}]")

class My91DownLoad():
    _favo_video_url = "https://0722.91p51.com/video.php?category=rf&page=1"  # https://0722.91p51.com/video.php?category=rf  分页
    _favo_video_url2 = "https://0722.91p51.com/index.php"  # https://0722.91p51.com/index.php 主页
    _current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    _current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def start(self, number: int = 0):
        """
        统一开始请求+下载入口
        :type number: int 下载个数，超过每页24 自动翻页
        :return:
        """
        list_urls = self.fetch_subpage_urls(number)

        list_videos, list_titles,list_images = self.fetch_video_urls(list_urls)

        self.download_videos(title_lists=list_titles,video_lists=list_videos)

    def fetch_subpage_urls(self, number: int = 0):
        """
        主入口:index页面去取得子详情页url
        number: 爬去subpage个数,每页最多24个。超过需翻页(未实现).默认:0-仅下载当前页24个
        :return:
        """
        pages = number // 24 + 1
        url_list = []
        ua=UserAgent()
        for page in range(pages):
            current_url = self._favo_video_url.replace("page=1", f"page={page + 1}")
            logger.info(f"current_url url : {current_url}")
            logger.info(f"start request index url : {current_url}")
            headers = {
                'User-Agent': ua.random,
                #'X-Forwarded-For': self.__random_ip()
                'Referer': current_url,
                #'cookie':'__cfduid=d4caf5fceb80b2ec8480f9bb5b3a5c7d41599484630; CLIPSHARE=r8fror5c7tdu7uoit2sagduuv2; __utmc=162791677; __utmz=162791677.1599484864.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __dtsu=10401599484639F90B58665C5A158ECD; __utma=162791677.328926869.1599484864.1599667047.1599745651.6; __utmb=162791677.0.10.1599745651'
            }
            res1 = requests.request('GET', current_url, headers=headers)
            logger.debug(f"res1.status_code : {res1.status_code}")
            logger.debug(f"res1.text include: {res1.text}")

            logger.info(f"start parse: get subpage urls:")
            # url_list=set()
            subpage_re_rules=[
                'https://0722.91p51.com/view_video.php\\?viewkey=.*&page=.*&viewtype=.*&category=.{2}',
                'temp'
            ]
            url_list_page = re.findall(subpage_re_rules[0],res1.text)
            url_list_set = list(set(url_list_page))
            # url_list=url_list_set
            for i in range(len(url_list_set)):
                url_list.append(url_list_set[i])

        if 0 < number <24:
            url_list=url_list[0:number]
            logger.debug(f"url_list[0:1] is: {url_list[0:1]}")
            logger.info(f"url_list 数量: {len(url_list)}")
            logger.debug(f"url_list is: {url_list}")

        return url_list

        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(1) > div > a
        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(2) > div > a
        # wrapper > div.container.container-minheight > div.row > div > div > div:nth-child(3) > div > a
        # // *[ @ id = "wrapper"] / div[1] / div[2] / div / div / div[1] / div / a
        # / html / body / div[4] / div[1] / div[2] / div / div / div[1] / div / a

        # number数大于每页最大个数 : 模拟分页按钮请求 实现翻页
        # self._fetch_specific_list(res1.text) #保存当前索引页到详情页链接，挨个去请求然后获取具体详情页viode链接

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
            logger.info(f"开始请求第[{i}]个subpage===>")
            ua = UserAgent()
            #  获取等video url 404: 需要解决这里的 cookies等加上获取等内容 == request获取内容
            # referer need user subpage url
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': ua.random,
                #'X-Forwarded-For': self.__random_ip(),
                'referer': listA[i],
                'Content-Type': 'multipart/form-data; session_language=cn_CN',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            res2 = requests.request('GET', listA[i], headers=headers)
            if res2.status_code != 200:
                logger.info(f"subpage url:[{listA[i]}] retrun an Error: status_code:[{res2.status_code}]")
                with open(self._current_day+'_request_subpage_failed.log','w',encoding='utf-8') as f:
                    f.write(f"\n请求失败的subpage_url:[{listA[i]}]\n\n")
            else:
                logger.info(f"subpage url:[{listA[i]}],status_code: [{res2.status_code}]")
                pass

            # with open(self._current_day+'_debug.log','a',encoding='utf-8') as f:
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
            url_re = list(set(url_re))

            if url_re:
                video_url = url_re[0]
                logger.info(f"video url:[{video_url}]")
                video_lists.append(video_url)
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
            else:
                logger.info(f"parse video url failed.please see error_log:{self._current_day + '_parse_video_url_error.log'}")
                with open(self._current_day + '_error.log', "a", encoding='utf-8') as f:
                    f.write(f"\n请求时间:[{self._current_time}]\n")
                    f.write(f"正则匹配失败subpage_url:[{listA[i]}]\n")
                    f.write(res2.text)
                    f.write("===============================================================================\n")
                # '''如果正常匹配条件没匹配到对应的视频url,则尝试匹配strencode函数解析对应视频url'''
                # strencode = re.findall(r'document.write\(strencode\("(.*)"', str(res2.text))
                # if not strencode:
                #     logger.info(f"第{i}个url:strencode() still parse failed,break.")
                #     break
                # else:
                #     # fecth video
                #     logger.info(f"第{i}个url:strencode() parse success.")
                #     temp = strencode[0].split(',')
                #     input = temp[0].replace('"', '')
                #     encode_key = temp[1].replace('"', '')
                #     video_url = self.__strdecode(input=input, key=encode_key)
                #     logger.info(f"第{i}个url解析出的video_url is:[{video_url}]")
            time.sleep(3)

        logger.info(f"共请求{len(listA)}个,成功请求[{len(video_lists)}]个...")
        with open(self._current_day+'_video_lists.log',"w") as f:
            f.write(self._current_time+':\n')
            for v in range(len(video_lists)):
                f.write(title_lists[v]+"\n"+video_lists[v]+"\n")

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
        assert video_lists, "video_lists为空"
        assert title_lists, "title_lists为空"
        # 创建文件夹
        storage_dir = self._current_day
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)
        else:
            pass

        for i in range(len(video_lists)):
            video_name = title_lists[i] + '.mp4'
            ua=UserAgent()
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
                'Referer':self._favo_video_url,
                # 'cookie':'',
            } # Referer？ video url不正确  #看一下对应的链接 请求头
            logger.info(f"共[{len(video_lists)}]个视频,开始下载第[{i}]个======>")
            res3 = requests.request('GET', url=video_lists[i], headers=headers)
            total_length = int(res3.headers.get("Content-Length"))
            logger.info(f"该文件大小:[{total_length//(1024*1024)}]M.")
            if res3.status_code != 200:
                logger.info(f"video download failed:[{video_lists[i]}] status_code:[{res3.status_code}]")
                break
            else:
                pass

            if os.path.exists(video_name):
                logger.info(f"video file: [{video_name}] already exist.")
                break
            else:
                logger.info(f"start download:[].")
                with open(storage_dir + '/' + video_name, "wb") as f:
                    #wdg = ['Progress: ', progressbar.Percentage(), ' ',progressbar.Bar(marker='#', left='[', right=']'),' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
                    # down_progress = ProgressBar(widgets=wdg, maxval=total_length).start()
                    down_progress = ProgressBar(maxval=total_length).start()
                    # down_progress.start()
                    for chunk in res3.iter_content(chunk_size=1):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                        down_progress.update(len(chunk) + 1)
                    down_progress.finish()
                logger.info(f"download success:[].")

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


if __name__ == '__main__':
    f = My91DownLoad()
    f.start(number=1)


