#!/usr/bin/python

def HammingDistance(a,b):
    val = a^b
    dis = 0
    while val:
        
        if val&1 == 1:
            dis+=1

        val=val>>1

    return dis

ret = HammingDistance(1,4)

print ret
