"""
门面模式:结构化模式
客户端 - 门面 - 子系统
"""

# add 子系统+ waiter 即可 避免过度依赖

class Client(object):
    def order(self):
        Waiter().make_set_meal()


class Waiter(object):
    def make_set_meal(self):
        Coke().make()
        Hamburger().make()


class Coke(object):
    def make(self):
        print("make Coke")


class Hamburger(object):
    def make(self):
        print("make Hamburger")


you = Client().order()
