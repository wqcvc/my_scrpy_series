"""
工厂模式
    1.简单工厂
    2.工厂方法
    3.抽象工厂
"""

import abc


class audi(object):
    def __repr__(self):
        return "audi"


class bmw(object):
    def __repr__(self):
        return "BMW"


# 1
class SimpleFactory(object):
    @staticmethod
    def product_car(name):
        if name == "audi":
            return audi()
        elif name == "bmw":
            return bmw()


c1 = SimpleFactory.product_car('audi')


# 2.
class AbstractFactory(metaclass=abc.ABCMeta):
    """
    抽象工厂
    """
    #  __metaclass__ = abc.ABCMeta equal to: metaclass = abc.ABCMeta
    @abc.abstractmethod
    def product_car(self):
        pass


class AudiFactory(AbstractFactory):
    def product_car(self):
        return audi()


class BMWFactory(AbstractFactory):
    def product_car(self):
        return bmw()


d1 = AudiFactory().product_car()
d2 = BMWFactory().product_car()


# 3.
# 两种小汽车
class Mercedes_C63(object):
    """梅赛德斯 C63
    """

    def __repr__(self):
        return "Mercedes-Benz: C63"


class BMW_M3(object):
    """宝马 M3
    """

    def __repr__(self):
        return "BMW: M3"


# 　两种SUV
class Mercedes_G63(object):
    """梅赛德斯 G63
    """

    def __repr__(self):
        return "Mercedes-Benz: G63"


class BMW_X5(object):
    """宝马 X5
    """

    def __repr__(self):
        return "BMW: X5"


class AbstractFactory2(object):
    """抽象工厂
    可以生产小汽车外，还可以生产SUV
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def product_car(self):
        pass

    @abc.abstractmethod
    def product_suv(self):
        pass


class MercedesFactory(AbstractFactory2):
    """梅赛德斯工厂
    """

    def product_car(self):
        return Mercedes_C63()

    def product_suv(self):
        return Mercedes_G63()


class BMWFactory(AbstractFactory2):
    """宝马工厂
    """

    def product_car(self):
        return BMW_M3()

    def product_suv(self):
        return BMW_X5()


c1 = MercedesFactory().product_car()
s1 = MercedesFactory().product_suv()
print(c1, s1)
s2 = BMWFactory().product_suv()
c2 = BMWFactory().product_car()
print(c2, s2)