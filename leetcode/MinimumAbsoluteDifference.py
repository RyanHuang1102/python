#!/usr/bin/python

def minimumAbsDifference(arr):
    """
    :type arr: List[int]
    :rtype: List[List[int]]
    """
    arr.sort()
    print arr
    ret = []
    size = len(arr)
    minimum = arr[1] - arr[0]

    for i in range(2,size):
        min = arr[i] - arr[i-1]
        if minimum > min:
            minimum = min

    for i in range(1,size):
        if minimum == arr[i] - arr[i-1]:
            ret.append([[arr[i-1], arr[i]]])
    return ret


arr = [4,8,3,1,6,-9]
ret = minimumAbsDifference(arr)
print ret
