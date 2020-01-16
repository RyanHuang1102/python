#!/usr/bin/python
#1047. Remove All Adjacent Duplicates In String    
def removeDuplicates(String):
    """
    :type String: str
    :rtype: str
    """
    ret = []
    for i in String: # empty list is False
        if ret and ret[-1] == i:
            ret.pop()
        else:
            ret.append(i)

    return "".join(ret)

str="abbaca"
ret = removeDuplicates(str)

print ret
        
