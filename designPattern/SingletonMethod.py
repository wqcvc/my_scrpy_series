"""
单例模式：只有1个特定类型的对象，用于日志记录 数据库操作
"""


class Singleton():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            # cls.instance = super(Singleton, cls).__new__(cls)
            cls.instance = super().__new__(cls)
            print("xxx")
        return cls.instance


s = Singleton()
print("Object created", s)

s1 = Singleton()
print("Object created", s1)
print(Singleton.__dict__)

"""
单例懒汉模式
"""


class Singleton2():
    __instance = None

    def __init__(self):
        if not Singleton2.__instance:
            print("__init__ method called...")
        else:
            print("Instance already created: ", self.getInstance())

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Singleton2()
        return cls.__instance


s2 = Singleton2()  # class inintialized, but object not created
# print("Object created", Singleton2.getInstance())  # object created here
# s3 = Singleton2()


"""
数据库 日志等应用 1 
"""
import sqlite3


class Metasingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super(Metasingleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Database(metaclass=Metasingleton):
    connection = None

    def connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()
        return self.cursorobj


# db1 = Database().connection()
# db2 = Database().connection()


"""
文件单例模式
"""
#mysingleton.py
class Singleton(object):
    def foo(self):
        pass
singleton = Singleton()

# other file
# from a import singleton