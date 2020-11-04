# -*- coding: utf-8 -*-
"""
 @Topic:简单封装个通用logger打印日志
    eg. 1.通用日志打印 继承or实例皆可
 @Date: 2020-10-12
 @Author: terry.wang
"""
import logging
# import datetime
import os
import io
import traceback
import sys


class MyLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(level=level)

        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(pathname)s %(funcName)s %(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')

        # console
        ch = logging.StreamHandler()
        ch.setLevel(level=level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # #file handler 暂时不用写入文件
        # path=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.log'
        # fh = logging.FileHandler(path)
        # fh.setLevel(level=level)
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    # def __get_cur_info(self):
    #     call_func=sys._getframe().f_code.co_name
    #     call_line=sys._getframe().f_lineno
    #     return call_func,call_line
    def findCaller(self, stack_info=False):
        """
        被调用的文件路径,函数和行号信息
        :param stack_info:
        :return:
        """
        f = logging.currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == __file__:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def test(self):
        """
        获取函数名及被调用函数名的3种方式 + 行数or 路径(to do)
        :return:
        """
        print(sys._getframe().f_code.co_name)
        print(sys._getframe(0).f_code.co_name)
        print(sys._getframe(1).f_code.co_name)
        print(sys._getframe(1).f_code.co_filename)
        # print(sys._getframe(1).f_back.f_lineno)


if __name__ == '__main__':
    mylogger = MyLogger(__name__, logging.INFO)
    mylogger.info(f"test mylogger func")
    mylogger.test()
