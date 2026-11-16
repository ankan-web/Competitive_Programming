class Solution:
    def maxSubArray(self, nums: list[int]) -> int:

        s = ms = nums[0]

        for x in nums[1:]:
            s = max(x, s + x)
            ms = max(s, ms)

        return ms
