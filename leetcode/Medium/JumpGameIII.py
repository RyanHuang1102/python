#!/usr/bin/python

def canReach(A, start, init):
    """
    A : List(int)
    start : int
    rtype : BOOL
    1306. Jump Game III
    """

    if 0<= start < len(A) and init[start] != -1:
        init[start] = -1
        print init
        return A[start] == 0 or canReach(A, start + A[start], init) or canReach(A, start - A[start], init)
    return False
A=[3,0,2,1,2]
init = [ 0 for i in range(len(A))]
ret = canReach(A, 4, init)
print ret
