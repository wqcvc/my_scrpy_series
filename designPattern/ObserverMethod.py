"""
观察者模式:

"""


# 看股票的职员
class StockClerk:
    def __init__(self, name):
        self.name = name

    def close_stock_software(self):
        print(f"{self.name} 关闭了股票软件，并开始办公")


# 睡着的职员
class SleepingClerk:
    def __init__(self, name):
        self.name = name

    def open_word(self):
        print(f"{self.name} 打开了word，并开始办公")


class Receptionist:
    actions = []

    @classmethod
    def attach(cls, action):
        cls.actions.append(action)

    @classmethod
    def notify(cls):
        print("老板回来了，各同事行动...")
        for actioin in cls.actions:
            actioin()


# 实例化职员
c1 = StockClerk('Chris')
c2 = SleepingClerk('Ryan')

# 告诉前台小姐姐如何通知
Receptionist.attach(c1.close_stock_software)
Receptionist.attach(c2.open_word)

# 前台小姐姐发布通知
Receptionist.notify()
