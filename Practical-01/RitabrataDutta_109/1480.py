class Solution:
    def runningSum(self, nums: list[int]) -> list[int]:

        sa = []
        s = 0

        for i in nums:
            s += i

            sa.append(s)

        return sa
