# -*- coding: utf-8 -*-
"""
 @Topic: 微信推送结果功能
    eg:
 @Date: 2021-1-13
 @Author: terry.wang
"""

from mylogger import logger
import itchat
itchat.login()

itchat.send(u'你好，文件传输助手','filehelper')
logger.info("test Singleton_logger method!")


class libWechatInfo(object):
    # sssq = lambda x: x * x
    # print(sssq(25))
    print((lambda s:s*s)(25))
    y= [x for x in range(4) if x%2]
    print(y)


if __name__ == "__main__":
    wchat = libWechatInfo()



