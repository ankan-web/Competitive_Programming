from collections import Counter


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:

        nH = set(nums)
        return len(nH) != len(nums)
