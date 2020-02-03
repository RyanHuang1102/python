#!/usr/bin/python

def smallestRangeI(A, K):
    """
    :type A: List[int]
    :type K: int
    :rtype: int
    """
    #ref http://www.noteanddata.com/leetcode-908-Smallest-Range-I.html
    return max(0,max(A)-min(A)-2*K)

A=[6,3,8]
K=2

ret = smallestRangeI(A,K)

print ret
