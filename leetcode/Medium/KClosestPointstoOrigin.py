#!/usr/bin/python
import heapq
def kClosest(points, K):
    """
    :type points: List[List[int]]
    :type K: int
    :rtype: List[List[int]]
    """
    return heapq.nsmallest(K, points, lambda (x, y): x * x + y * y)

def kClosest2(points, K):
    points.sort(key= lambda (x, y): x * x + y * y)

    while len(points) > K:
        points.pop(len(points)-1)

    return points

points = [[-2,4],[5,1],[3,3]]
ret = kClosest2(points, 2)
print ret
