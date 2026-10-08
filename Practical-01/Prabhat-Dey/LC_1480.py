#1480. Running Sum of 1d Array

class Solution(object):
    def runningSum(self, nums):
        for i in range(1,len(nums)):
            nums[i]=nums[i]+nums[i-1]
        return nums

        