1.分别匹配出来，存入字典，看是否是正确的配对
res1 = re.findall('<img class="img-responsive" src="https://i.test22.net/thumb/(.*?).jpg"/>', str(strr))
res2 = re.findall('<span class="video-title title-truncate m-t-5">(.*?)</span>', str(strr))

2.字典操作
dict_a = {}
for i in range(len(res1)):
    dict_a[res2[i]] = res1[i]
print(dict_a)
print(type(dict_a))
3.下载img 

4.合并ts文件到1个

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File : test_re.py
Func : 
Author : qi.wang02@msxf.com
Date : 2021/9/26 9:56
"""

import re

with open('test_re.html', 'r') as f:
    strr = f.readlines()

print(strr)
res1 = re.findall('<img class="img-responsive" src="https://i.test22.net/thumb/(.*?).jpg"/>', str(strr))
res2 = re.findall('<span class="video-title title-truncate m-t-5">(.*?)</span>', str(strr))

print(res1)
print(res2)

dict_a = {}
for i in range(len(res1)):
    dict_a[res2[i]] = res1[i]

print(dict_a)
print(type(dict_a))

import os


def heBingTsVideo(download_path, hebing_path):
    all_ts = os.listdir(download_path)
    with open(hebing_path, 'wb+') as f:
        for i in range(len(all_ts)):
            ts_video_path = os.path.join(download_path, all_ts[i])
            f.write(open(ts_video_path, 'rb').read())
    print("合并完成！！")


download_path = r"C:\Users\Administrator\Desktop\AiShu\下载视频\TS视频"
hebing_path = r"C:\Users\Administrator\Desktop\AiShu\下载视频\合并TS视频\第一财经.mp4"
heBingTsVideo(download_path, hebing_path)

os.chdir(hebing_path)
# print(shell_str)
shell_str1 = 'copy /b *.ts ' + 'xxx.mp4'
shell_str2 = 'del *.ts'
os.system(shell_str1)
os.system(shell_str2)
print(shell_str1, shell_str2)

