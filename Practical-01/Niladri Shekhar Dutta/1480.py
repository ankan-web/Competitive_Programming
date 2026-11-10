class Solution:
    def runningSum(self, nums: list[int]) -> list[int]:
        ans = []
        total = 0

        for num in nums:
            total += num
            ans.append(total)

        return ans