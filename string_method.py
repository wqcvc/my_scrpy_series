# -*- coding:utf-8 -*-
"""
字符串常用操作: 查找是否存在  反转 统计出现次数最高/指定 去除
"""


# 1. 字符串查找： A 中 find B 次数
class Solution2:
    def maxRepeating2(self, sequence: str, word: str) -> int:
        flag = 0
        s = word
        while s in sequence:
            flag += 1
            s += word
            print(s)
        return flag


# ss1 = "aaabaaaabaaabaaaabaaaabaaaabaaaaba"
# ss2 = "aaaba"
#
# ss3 = Solution2()
# ress3 = ss3.maxRepeating2(ss1,ss2)
# print(ress3)
import collections
from collections import Counter
import re


# 2. 字符串反转
class Solution:
    def reverseString(self, s: list) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        right = len(s) - 1
        left = 0
        times = (right + left) // 2
        print(times)
        for i in range(times):
            s[right], s[left] = s[left], s[right]
            right -= 1
            left += 1
            print(f"i is :[{i}]")
        return s

    def mostCommonWord(self, paragraph, banned):
        """
        :type paragraph: str
        :type banned: List[str]
        :rtype: str
        """
        paragraph = collections.Counter(re.findall('[a-z]+', paragraph.lower()))
        for i in paragraph.most_common():
            if i[0] in banned:
                continue
            return i[0]

    def buddyStrings(self, s, goal):
        """
        :type s: str
        :type goal: str
        :rtype: bool
        """
        if len(s) != len(goal):
            return False
        if s == goal and len(set(s)) < len(s):
            return True
        diff = []
        for i in range(len(s)):
            print(i)
            if s[i] != goal[i]:
                diff.append(i)
        if len(diff) == 2:
            return True if s[diff[0]] == goal[diff[1]] and s[diff[1]] == goal[diff[0]] else False
        else:
            return False

    def indexPairs(self, text, words):
        """
        :type text: str
        :type words: List[str]
        :rtype: List[List[int]]
        """
        list1 = []
        for i in words:
            j = 0
            while j < len(text):
                index = text.find(i, j)
                print(index)
                tmp = [index, index - 1 + len(i)]
                if tmp not in list1:
                    list1.append(tmp)
                j += 1
        list1.sort()
        return list1

    def areNumbersAscending(self, s):
        """
        :type s: str
        :rtype: bool
        """
        kk = s.split()
        for k in kk:
            tmp = 0
            if k.isdigit():
                if int(k) > tmp:
                    print(tmp)
                else:
                    return False
                tmp = int(k)
        return True

    def countVowelSubstrings(self, word):
        """
        :type word: str
        :rtype: int
        """
        ex = 'aeiou'
        list1 = []
        s = ''
        for i in range(len(word)):
            if word[i] in ex:
                s += word[i]
            else:
                if len(s) >= 5:
                    print(s)
                    list1.append(s)
                else:
                    s = ''
        if not list1:
            return 0
        count = 0
        for j in list1:
            count += (len(j) - 4) * (len(j) - 4) / 2
        return count

    def checkAlmostEquivalent(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: bool
        """
        cw1 = Counter(word1)
        cw2 = Counter(word2)
        cw3 = cw1 - cw2
        cw4 = cw2 - cw1
        print(cw3)
        print(cw4)
        for i in cw3.values():
            if abs(i) > 3:
                return False
        for i in cw4.values():
            if abs(i) > 3:
                return False
        return True

    def quickSort(self, listA):
        """
        快速排序 递归 选定结束条件
        :param listA:
        :return:
        """
        if len(listA) <= 1:
            return listA
        else:
            flag = listA[0]
            less = []
            bigger = []
            for i in range(1, len(listA)):
                if listA[i] < flag:
                    less.append(listA[i])
            for i in range(1, len(listA)):
                if listA[i] > flag:
                    bigger.append(listA[i])
            print(f"less:[{less}]")
            print(f"bigger:[{bigger}]")
            print("---------------")
            return self.quickSort(less) + [flag] + self.quickSort(bigger)

    def selectSort(self, listA):
        """
        选择排序: 将剩余未排序的选出最小值，记录下标并交换即可
        :param listA:
        :return:
        """
        for i in range(len(listA)):
            min = i
            for j in range(i + 1, len(listA)):
                if listA[j] < listA[min]:
                    min = j
            listA[min], listA[i] = listA[i], listA[min]
        return listA

    def bucketSort(self, listA):
        """
        桶排序  按照最大值n分配n个桶，将对应的值放入对应值下标的桶中
        :param listA:
        :return:
        """
        nums = max(listA)
        bucket = [0] * (nums + 1)
        for i in listA:
            bucket[i] += 1

        res1 = []
        for i in range(len(bucket)):
            if bucket[i] != 0:
                for times in range(bucket[i]):
                    res1.append(i)
        return res1

    def bubbleSort(self, listA):
        """
        冒泡：比较相邻的2个元素 不停的做交换.缩小范围
        :param listA:
        :return:
        """
        for i in range(len(listA)):
            for j in range(len(listA)-1):
                print(len(listA)-1)
                if listA[j] > listA[j + 1]:
                    listA[j], listA[j + 1] = listA[j + 1], listA[j]
            print(listA)
        return listA


ss1 = Solution()
# list1 = [6, 3, 5, 7, 1, 9, 2, 4, 8, 0, 2, 3, 13, 12]
list1 = [6, 3, 5,2]
res1 = ss1.bubbleSort(list1)
print(res1)
