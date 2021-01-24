# -*- coding: utf-8 -*-
"""
 @Topic:写一个单例模式的logger类
    eg. 直接其他模块 import 实例类 使用即可
 @Date: 2021-1-13
 @Author: terry.wang
"""
import logging
import logging.handlers
import datetime

logger = logging.getLogger(name="my_logger")

__current_day = datetime.datetime.now().strftime("%Y%m%d")
LOG_FILENAME = f"./log_{__current_day}.log"


def set_Logger():
    logger.setLevel(level=logging.INFO)
    fformatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                   '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fformatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(fformatter)
    logger.addHandler(file_handler)


set_Logger()
