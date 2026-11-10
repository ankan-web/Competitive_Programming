class Solution(object):
    def twoSum(self, nums, target):
        hashmap={}
        for i in range(len(nums)):
            num=target-nums[i]
            if num in hashmap:
                return [hashmap[num],i]
            hashmap[nums[i]] = i
                