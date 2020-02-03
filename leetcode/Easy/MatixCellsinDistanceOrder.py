#!/usr/bin/python

def allCellsDistOrder(R, C, r0, c0):
    """
    R:row
    C:column
    r0,c0: start
    """
    def dist(point):
        pi,pj = point
        return abs(pi - r0) + abs(pj - c0)

    points = [(i, j) for i in range(R) for j in range(C)]
    return sorted(points, key=dist)

R=2
C=3
ret = allCellsDistOrder(R,C,1,2)

print ret
