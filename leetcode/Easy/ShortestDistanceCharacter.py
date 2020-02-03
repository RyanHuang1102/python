#!/usr/bin/python

def shortestToChar(S, C):
    """
    :type S: str
    :type C: str
    :rtype: List[int]
    821. Shortest Distance to a Character
    """
    n = len(S)
    res = [0 if c == C else n for c in S]
    for i in range(n - 1): 
	res[i + 1] = min(res[i + 1], res[i] + 1)
    for i in range(n - 1)[::-1]: 
	res[i] = min(res[i], res[i + 1] + 1)
    
    return res

string = "loveleetcode"
res = shortestToChar(string, "e")

print res
