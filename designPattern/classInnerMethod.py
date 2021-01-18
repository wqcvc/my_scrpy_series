# -*- coding: utf-8 -*-

"""
python class 内置方法
"""

"""
0. Python有3种方法，
   静态方法（staticmethod）: 无需实例化就可以直接调用 @staticmethod。 函数嵌入到类中的一种方式，函数就属于类，同时表明函数不需要访问这个类。通过子类的继承覆盖，能更好的组织代码。
   类方法（classmethod):  @classmethod 修饰的方法需要通过cls参数传递当前类对象。非强制，即通常用self来传递当前类对象的实例，cls传递当前类对象
                         @staticmethod和@classmethod都可以直接类名.方法名()来调用
   实例方法
"""


class A(object):
    bar = 1

    def foo(self):
        print("foo")

    @staticmethod
    def static_foo():
        """
        要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名
        :return:
        """
        print("static_foo")
        print(A.bar)

    @classmethod
    def class_foo(cls):
        """
        因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码
        :return:
        """
        print("class_foo")
        print(cls.bar)
        cls().foo()


A.static_foo()
a = A()

"""
1.__init__():
  __init__方法在类的一个对象被建立时，马上运行。这个方法可以用来对你的对象做一些你希望的初始化
"""


class Person(object):
    def __init__(self, name, age):
        print("person __init__")
        self.name = name
        self.age = age

    def sayhi(self):
        print(self.name, self.age)


p1 = Person('test', 28)
p1.sayhi()

"""
2.__new()__
    __new__()在__init__()之前被调用，用于生成实例对象. 是静态方式staticmethod
    __new__() 是在新式类中新出现的方法，它作用在构造方法建造实例之前，可以这么理解，在 Python 中存在于类里面的构造方法 __init__() 负责将类的实例化，
  而在 __init__() 启动之前，__new__() 决定是否要使用该 __init__() 方法，因为__new__() 可以调用其他类的构造方法或者直接返回别的对象来作为本类的实例。
    通常来说，当前类开始实例化时，new()方法会返回cls（cls指代当前类）的实例，然后该类的init()方法作为构造方法会接收这个实例（即self）作为自己的第一个参数，
  然后依次传入new ()方法中接收的位置参数和命名参数。
  注意：如果new()没有返回cls（即当前类）的实例，那么当前类的init()方法是不会被调用的
    如果new()返回其他类的实例，那么只会调用被返回的那个类的构造方法。
  因此可以这么描述new()和ini()的区别，在新式类中new()才是真正的实例化方法，为类提供外壳制造出实例框架,然后调用该框架内的构造方法init()使其丰满
  如果以建房子做比喻，new()方法负责开发地皮，打下地基，并将原料存放在工地
  而init()方法负责从工地取材料建造出地皮开发招标书中规定的大楼，init()负责大楼的细节设计，建造，装修使其可交付给客户
"""
class Person2(object):
    def __init__(self):
        print("Person2 __init__")
        self.name = 'Person2_name'

    def __new__(cls, *args, **kwargs):
        print("__new__")
        ob = object.__new__(Person)  #  object or 父类实例
        ob.__init__(name='222',age=22)
        print(ob)
        return ob


p2 = Person2()
print(p2.name)


"""
  3.__getattr__()、__setattr__()和__getattribute__()  
  当读取对象的某个属性时，python会自动调用__getattr__()方法.例如，fruit.color将转换为fruit.__getattr__(color).当使用赋值语句对属性进行设置时，
  python会自动调用__setattr__()方法.__getattribute__()的功能与__getattr__()类似，用于获取属性的值.但是__getattribute__()能提供更好的控制，代码更健壮.
  注意，python中并不存在__setattribute__()方法.
  __getattr__(self, item):在访问对象的 item 属性且 item 属性不存在时会调用此方法，如果对象已经有 item 这个属性了，则不会调用这个方法，会直接返回对象的 item 属性
  __setattr__():如果该属性不存在，则会调用__setattr__()对实例属性赋值，被赋值的属性和值会存入实例属性字典__dict__中
  __getattribute__(self, item):访问对象的任何属性，不管存不存在，都会调用此方法.同时存在只调用此方法
  __delattr__:
  setattr() getattr() hasattr()
"""
"""
  4. __dict__:存储对象的属性 
  类__dict__: 所有类属性组成的字典
  实例__dict__: 类中所有实例属性组成的字典
    __doc__()     
    __module__
"""
"""
  5.__getitem__()
  实例对象（假设为P）就可以这样P[key]取值。当实例对象做P[key]运算时，就会调用类中的__getitem__()方法。
  __delitem__ : 这个方法在对对象的组成部分使用__del__语句的时候被调用，应删除与key相关联的值。同样，仅当对象可变的时候，才需要实现这个方法。
"""
"""
  6.__call__():
  即 __call__()。该方法的功能类似于在类中重载 () 运算符，使得类实例对象可以像调用普通函数那样，以“对象名()”的形式使用。
"""
"""
  7.__name__: self.__class__.__name__ 实例对应的类的类名
"""

res = getattr(a,'bar')
print(res)


class Person3(object):
    """to test __doc__()"""

    def __init__(self):
        self.name = 'wq123'
        self.age = '123'
        print("xxxx")
        print(self.__class__)
        print(self.__class__.__name__)

    def __getattr__(self, item):
        return 'in __getattr__() 未找到属性：'+item

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    # def __getattribute__(self, item):
    #     print("in __getattribute__() method")
    #     return object.__getattribute__(self,item)

    def __getitem__(self, item):
        if item == self.name:
            return self.age
        else:
            return '__getitem__()'

    def __delitem__(self, key):
        print('调用delitem')
        del self.change[key]

    def __delattr__(self, item):
        print(f"execute __delattr__:item={item}")
        super().__delattr__(item)

    def __call__(self, *args, **kwargs):
        """
        使类的实例对象变为可以调用
        :return:
        """
        print(f"调用_call__()方法:*args:[{args}].**kwargs:[{kwargs}]")


    def __str__(self):
        """
        返回一个对象的描述信息
        print(实例)
        """
        return "名字是:%s , 年龄是:%d" % (self.name, self.age)

    def __del__(self):
        """
        析构函数 对象销毁的时候执行
        :return:
        """
        print("__del__")
        pass

    def __repr__(self):
        """
        类似 str()
        """
        pass

    #issubclass isinstance



p3 = Person3()
print(p3.__dict__)
print(Person3.__dict__)
print(p3.name)
print(p3.loop)
p3.loll = 23
print(p3.loll)
print(p3.__dict__)

print(p3['wq123'])
print(Person3.__doc__)
print(p3.__dir__())

p3(1,"s1",k=2,s2="s2")
print(f"type of Person3: [{type(Person3)}]")


"""
  lambda匿名函数  
  []列表推导式
"""
add = lambda x,y:x+y
print(add(2,3))

l1 = [i*2 for i in range(1,10) if i > 2]
print(l1)
# 太复杂的不推荐使用


"""
    元类: metaclass
    metaclass 可以像装饰器那样定制和修改继承它的子类 黑魔法
"""

