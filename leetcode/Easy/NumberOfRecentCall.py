#!/usr/bin/python

class RecentCounter(object):
    def __init__(self):
        self.ping_c = 0
        self.list = []
    def ping(self, t):
        self.list.append(t)
        list_len = len(self.list)

        if (self.list[list_len-1] - self.list[0])<=3000:
            self.ping_c+=1
        else:
            pass

        return self.ping_c

obj = RecentCounter()
ret = obj.ping(1)
print "ret first:%d" %(ret)
obj.ping(2)
obj.ping(3001)
ret = obj.ping(3002)
print "ret last:%d" %(ret)
