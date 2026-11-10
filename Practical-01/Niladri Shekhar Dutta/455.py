class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        g.sort()
        s.sort()

        i = 0
        j = 0
        ans = 0

        while i < len(g) and j < len(s):
            if s[j] >= g[i]:
                ans += 1
                i += 1

            j += 1

        return ans