#!/usr/bin/python

class Solution(object):
    def __init__(self):
        self.dic = {}
    def uniqueOccurrences(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """
        for i in arr:
            if i not in self.dic:
                self.dic[i]=1
            else:
                self.dic[i]+=1
        #print self.dic
        return len(self.dic) == len(set((self.dic).values()))

arr = [1,2,2,1,1,3,3]
ret = Solution().uniqueOccurrences(arr)

print ret

