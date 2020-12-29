# -*- coding:utf-8 -*-
"""
字符串常用操作: 查找是否存在  反转 统计出现次数最高/指定 去除
"""

# 1. 字符串查找： A 中 find B 次数
class Solution2:
    def maxRepeating(self, sequence: str, word: str) -> int:
        times = 0
        if word in sequence:
            times = sequence.count(word)
        return times

    def maxRepeating2(self, sequence: str, word: str) -> int:
        flag = 0
        s = word
        while s in sequence:
            flag+=1
            s+=word
            print(s)
        return flag

    def maxRepeating3(self, sequence: str, word: str) -> int:
        res = 0
        for i in range(len(sequence)//len(word)+1):
            temp = word *(i+1)
            print(temp)
            if temp in sequence:
                res += 1
            else:
                return res




ss1 = "aaabaaaabaaabaaaabaaaabaaaabaaaaba"
ss2 = "aaaba"

ss3 = Solution2()
ress3 = ss3.maxRepeating2(ss1,ss2)
print(ress3)

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

# s = ["h", "e", "l", "l", "o"]
#
# s1 = Solution()
# res = s1.reverseString(s)
# print(res)


