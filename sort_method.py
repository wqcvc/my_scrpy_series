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
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    print(f"bubble_sort res: " + str(lista))


bubble_sort(listA)


#  2.插入排序
#
def insert_sort(li: list):
    assert li, "li不能为空"
    for i in range(len(li)):
        j = i - 1
        while j >= 0 and li[j] > li[i]:
            li[j+1] = li[j]
            j -=1
        li[j+1] = li[i]
    print(li)

insert_sort(listA)




