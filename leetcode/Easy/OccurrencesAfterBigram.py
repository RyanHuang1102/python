#!/usr/bin/python

"""
1078. Occurrences After Bigram
"""
def findOcurrences(text, first, second):
    """
    :type text: str
    :type first: str
    :type second: str
    :rtype: List[str]
    """
    c = text.split()
    ret = []
    for i in range(2, len(c)):
        if c[i-2] == first and c[i-1] == second:
            ret.append(c[i])
    return ret

string = "alice is a good girl she is a good student"
first = "a"
second = "good"
ret = findOcurrences(string, first, second)

print ret
