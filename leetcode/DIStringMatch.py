#!/usr/bin/python

class Solution(object):
    def diStringMatch(self, S):
        """
        :type S: str
        :rtype: List[int]
        """
        increase = 0 
	decrease = len(S)
        res = []
        for i in S:
            if i == "I":
                res.append(increase)
                increase += 1
            else:
                res.append(decrease)
                decrease -= 1

	res.append(decrease)
	print res
	

S=["I","D"]

Solution().diStringMatch(S)
