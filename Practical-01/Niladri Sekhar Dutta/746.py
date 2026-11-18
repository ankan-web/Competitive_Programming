from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp0 = dp1 = 0
        for i in range(2, n + 1):
            cur = min(dp0 + cost[i - 2], dp1 + cost[i - 1])
            dp0, dp1 = dp1, cur
        return dp1