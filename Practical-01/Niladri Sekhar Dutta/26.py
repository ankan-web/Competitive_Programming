from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        write = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[write - 1]:
                nums[write] = nums[i]
                write += 1
        return write