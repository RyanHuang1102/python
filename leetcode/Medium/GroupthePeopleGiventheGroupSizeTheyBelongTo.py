#!/usr/bin/python
import collections
def groupTheoPeople(groupSizes):
    """
    type gruopSize: List[int]
    rype: List[List[int]]
    1282. Group the People Given the Group Size They Belong To
    """
    dic = collections.defaultdict(list)
    for i, key in enumerate(groupSizes):
        dic[key].append(i)

    return [index[i:i+size] for size,index in dic.items() for i in xrange(0,len(index), size)]

    """
    for size,index in dic.items():
        print size,index
        for i in xrange(0,len(index), size):
            print i
            print index[i:i+size]
    """

group = [3,3,3,3,3,1,3]
ret = groupTheoPeople(group)
print ret
