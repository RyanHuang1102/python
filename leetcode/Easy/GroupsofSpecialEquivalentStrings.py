#!/usr/bin/python

def numSpecialEquivGroups(A):
    """
    :type A:List[str]
    :rtype: int
    """
    return len(set("".join(sorted(s[0::2])) + "".join(sorted(s[1::2])) for s in A))

A=["abcd","cdab","cbad","xyzz","zzxy","zzyx"]
ret = numSpecialEquivGroups(A)
print ret
