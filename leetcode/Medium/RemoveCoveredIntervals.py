#!/usr/bin/python

def removeCoveredIntervals(intervals):
    """
    1288. Remove Covered Intervals
    """
    intervals.sort()
    print intervals
    intervals.sort(key = lambda a:(a[0], -a[1]))
    print intervals
    res = right = 0
    for i,j in intervals:
        res+=j > right
        right = max(j,right)
    print res
    return res

intervals=[[1,4],[3,6],[2,8],[2,9],[3,10]]
removeCoveredIntervals(intervals)
