#!/usr/bin/python

class Soulution():
    def findNmbers(self, nums):
        """
        Input: nums = [12,345,2,6,7896]
        Output: 2
        Explanation: 
        12 contains 2 digits (even number of digits). 
        345 contains 3 digits (odd number of digits). 
        2 contains 1 digit (odd number of digits). 
        6 contains 1 digit (odd number of digits). 
        7896 contains 4 digits (even number of digits). 
        Therefore only 12 and 7896 contain an even number of digits.
        """
        ret = 0
        for var in nums:
            
            if len(str(var))%2 == 0:
                ret+=1
        return ret

nums=[12, 345, 2, 6, 7896]
ret = Soulution().findNmbers(nums)
print ret

