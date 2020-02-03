#!/usr/bin/python 

class Solution():
    def arrayPairSum(self, nums):
        """
        Input: [1,4,3,2]
        maximum sum of pairs is 4 = min(1, 2) + min(3, 4)
        """
        sort = sorted(nums)
        buf = 0
        count = 0
        
        while count < len(nums):
            buf+=nums[count]
            count+=2
        return buf

nums = [1,4,3,2,5,6]
ret = Solution().arrayPairSum(nums)
print ret
