"""
代理模式:
 跟 门面模式有类似 一个封装整个对象 一个封装对外提供接口？
"""


class You:
    def __init__(self):
        print(f"You:: lets buy the shrit!")
        self.debitCard = DebitCard()
        self.isPurchased = None

    def make_payment(self):
        self.isPurchased = self.debitCard.do_pay()


class DebitCard:
    def __init__(self):
        print(f"DebitCard:!")

    def do_pay(self):
        print(f"DebitCard : do_pay!")


you = You()
you.make_payment()
