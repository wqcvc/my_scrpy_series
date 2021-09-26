# -*- coding: utf-8 -*-
"""
排序算法合集
"""

listA = [9, 8, 7, 6, 5, 4, 3, 2, 1]


#  1. 冒泡排序 O(n²)-O(n)
#  相邻2个挨个比较更换顺序
def bubble_sort(lista: list):
    assert lista, "lista入参不能为空"
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            if lista[j] > lista[j + 1]:
                lista[j + 1], lista[j] = lista[j], lista[j + 1]
        print(lista)

    print(f"bubble_sort res: " + str(lista))


# bubble_sort(listA)


#  2.插入排序 O(n²)-O(n)
#  划分排序区和未排序区进行排序
def insert_sort(li: list):
    assert li, "li不能为空"
    for i in range(len(li)):
        j = i - 1
        m = li[i]  # m记录了每次选中的需要排序的值
        while j >= 0 and li[j] > m:  # j的位置循环往前搜索一直比较m和前面的每个值进行排序
            li[j + 1] = li[j]  # 如果符合while条件 就代表大小不对，需要交换m和 li[j]的值。如此循环
            li[j] = m
            j -= 1
            print(li)
    print(li)


# insert_sort(listA)


#  3.快速排序 O(n²)-O(nlogn)
#  递归 基准比较左右移动。小的左边 大的右侧。
# def quick_sort(li):
#     le = len(li)
#     if le <= 1:
#         return li
#     else:
#         f = li[0]
#         less = [x for x in li[1:] if f >= x]
#         gree = [x for x in li[1:] if f < x]
#         print(li)
#         return quick_sort(less) + [f] + quick_sort(gree)
def quick_sort(li):
    length = len(li)
    if length <= 1:
        return li
    else:
        flag = li[0]
        less, greater = [], []
        for i in li[1:]:
            if i >= flag:
                greater.append(i)
        for j in li[1:]:
            if j < flag:
                less.append(j)
        return quick_sort(less) + [flag] + quick_sort(greater)


# aa = quick_sort(listA)
# print(aa)


#  4.选择排序 O(n²)-O(n²)
#  选择最小or最大的往前放置依次排序
def select_sort(li):
    assert li, "li为空，请检查"
    for i in range(len(li)):
        min = i  # min 不能设置为 li[i]
        for j in range(i + 1, len(li)):
            if li[min] > li[j]:
                min = j
        li[min], li[i] = li[i], li[min]
    print(li)


# select_sort(listA)

#  5.桶排序 O(n)
#  待排数据分到多个有序桶，桶里排序然后依次取出完成排序
def bucket_Sort(li):
    maxnum = max(li)

    bucket_li = [0] * (maxnum + 1)

    for i in li:
        bucket_li[i] += 1

    sort_li = []
    for i in range(len(bucket_li)):
        if bucket_li[i] != 0:
            for times in range(bucket_li[i]):  # 值的次数有几次记录下来
                sort_li.append(i)
                print(sort_li)
    print(sort_li)


# bucket_Sort(listA)

listB = [8, 4, 3, 1]


#  1. 冒泡排序 O(n²)-O(n)
#  相邻2个挨个比较更换顺序
def bubble_sort2(li):
    for i in range(len(li)):
        for j in range(len(li) - 1):
            if li[j + 1] < li[j]:
                li[j + 1], li[j] = li[j], li[j + 1]
                print(li)
    print(li)


# bubble_sort2(listB)

# 2
# 排序区与 未排序区
def insert_sort2(li):
    for i in range(len(li)):
        j = i - 1
        k = li[i]
        while j >= 0 and li[j] > k:
            li[j + 1] = li[j]
            li[j] = k
            j -= 1
        print(li)
    print(li)


# insert_sort2(listB)

# 3 快速排序
# 递归
def quick_sort2(li):
    ll = len(li)
    if ll <= 1:
        return li
    else:
        flag = li[0]
        less = [x for x in li[1:] if flag >= x]
        greater = [x for x in li[1:] if flag < x]

        return quick_sort(less) + [flag] + quick_sort(greater)


# print(quick_sort2(listB))


# 4.选择排序
# 找最小的往左放
def select_sort2(li):
    for i in range(len(li)):
        min = i
        for j in range(i, len(li)):
            if li[min] > li[j]:
                min = j
        li[min], li[i] = li[i], li[min]
    print(li)
    print("xxx")


# select_sort2(listB)


# 5.桶排序

def bucket_sort2(li):
    num = max(li)

    bucket = [0] * (num + 1)

    for i in li:  # 对应的li的值 在bucket列表对应的 i值 中 +1，eg: li[0] = 4。在bucket[4]的0会统计+1
        bucket[i] += 1

    sort = []
    for j in range(len(bucket)):
        if bucket[j] != 0:
            for x in range(bucket[j]):
                sort.append(j)

    print(sort)
    print("x2x2x2")

listC = [6, 4, 3, 8, 7, 1, 26]
# bucket_sort2(listC)

# 查找： 顺序查找 二分查找
#####################################################

listD = [8, 4, 1, 3, 2, 5]
def bubble_sort3(li):
    for i in range(len(li)):
        for j in range(len(li)):
            if li[j] > li[i]:
                li[j],li[i] = li[i],li[j]
    print("bubble_sort3 : listD")
    print(li)

# bubble_sort3(listD)

def insert_sort3(li):
    for i in range(len(li)):
        var =  li[i]
        j = i - 1
        while j>=0 and li[j] < var:
            li[j+1] = li[j]
            li[j] = var
            j -= 1
    print("insert_sort3 listdddD")
    print(li)

# insert_sort3(listD)

def select_sort3(li):
    for i in range(len(li)):
        min = i
        for j in range(i,len(li)):
            if li[min] > li[j]:
                min = j
        li[min],li[i] = li[i],li[min]
    print("select_sort3 listDDDDD")
    print(li)

# select_sort3(listD)


def quick_sort3(li):
    length = len(li)
    if length <=1:
        return li
    else:
        flag = li[0]
        less = [x for x in li[1:] if x<flag]
        greater = [x for x in li[1:] if x> flag ]
        return quick_sort3(less) + [flag] + quick_sort3(greater)

# print(f"quick_sort3:"+str(quick_sort3(listD)))



def bucket_sort3(li):
    length = max(li)

    buckect_list = [0] * (length + 1 )
    for i in li:
        buckect_list[i] += 1

    sort = []
    for i in range(len(buckect_list)):
        if buckect_list[i] != 0:
            for j in range(buckect_list[i]):
                sort.append(i)

    print("DDDDD")
    print(sort)


bucket_sort3(listD)





# bucket_sort3(listD)

#  查找算法
#  顺序查找
#  二分查找

def sequential_search(li, key):
    flag = False
    for i in range(len(li)):
        if li[i] == key:
            flag = True

    return flag


listF = [1, 2, 3, 4, 5,6,7,8,9,10]
key = 10
# 二分查找
def search_half(li:list,target):
    lenth = len(li)
    left = 0
    right = lenth - 1
    while right >= left:
        middle = (right + left) // 2
        if li[middle] > target:
            right = middle - 1
        elif li[middle] < target:
            left = middle + 1
        else:
            print(f"target location is: [{middle}]")
            return
    return -1
# search_half(listF,key)


# 闰年
def runnian(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        print(f"year:[{year}] 是闰年！")
    else:
        print("xxxx")


# runnian(1900)


# 质数

def zhishu(num: int):
    if num > 1:
        for i in range(2, num):
            if num % i == 0:
                print(f"not zhishu")
                break
            else:
                print("yes zhishu")
                break


# zhishu(22)


# 斐波拉切数列
def fib_func(n:int):
    if n == 1 or n == 2:
        return 1
    else:
        return fib_func(n-1) + fib_func(n-2)


fib_list = [0]
for i in range(1,10):
    fib_list.append(fib_func(i))
# print(fib_list)













