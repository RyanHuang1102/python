#!/usr/bin/python

class Solution(object):
    def sortedSquares(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        for i in range(len(A)):
            A[i] *= A[i]
        A.sort()
        return A
A = [-4, -1, 0, 3, 10]

ret = Solution().sortedSquares(A)

print ret
