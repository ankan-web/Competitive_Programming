class Solution:
    def maxProfit(self, prices: list[int]) -> int:

        i, j = 0, 0
        prof = 0

        while i < len(prices):
            curr_prof = prices[i] - prices[j]
            if curr_prof < 0:
                j = i
            if curr_prof >= 0:
                prof = max(curr_prof, prof)

            i += 1

        return prof
