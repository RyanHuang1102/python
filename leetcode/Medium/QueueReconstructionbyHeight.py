#!/usr/bin/python

def reconstructQueue(people):
    """
    :type people: List[List[int]]
    :rtype: List[List[int]]
    406. Queue Reconstruction by Height
    """
    people.sort(key = lambda x: (-x[0], x[1]))# sort -x[0] first (large -> small) and then x[1](small->large)
    print people
    res=[]
    for p in people:
        res.insert(p[1], p)
    print res


p_list=[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]
reconstructQueue(p_list)
