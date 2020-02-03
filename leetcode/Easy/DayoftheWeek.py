#!/usr/bin/python

def dayOfTheWeek(d, m, y):
    """
    :type day: int
    :type month: int
    :type year: int
    :rtype: str
    Zeller's congruence
    1185. Day of the week
    """
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if d > 31 or (m == 2 and d > 29):
        print "pls check the day!"
        return

    if m > 12:
        print "check the month!"
        return 

    if m < 3:
        m+=12
        y-=1
    
    c,y = y/100, y%100
    w = (c / 4 - 2 * c + y + y / 4 + 13 * (m + 1) / 5 + d - 1) % 7
    print days[w]
    return days[w]

ret = dayOfTheWeek(21,1,2020)


