#!/usr/bin/python

def dailyTemperatures(T):
    """
    :type T: List[int]
    :rtype: List[int]
    739. Daily Temperatures(medium)
    """
    n = len(T)
    ret = []
    start = 1
    for i in range(n):
        for j in range(start,n):
            if T[i] < T[j]:
                ret.append(j-i)
                start+=1
                break
            if j == n-1:
                ret.append(0)
    print ret

temp = [73, 74, 75, 71, 69, 72, 76, 73]
dailyTemperatures(temp)
