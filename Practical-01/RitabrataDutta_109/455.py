class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:

        g.sort()
        s.sort()

        gI, sI = 0, 0

        while sI < len(s) and gI < len(g):
            if g[gI] <= s[sI]:
                gI += 1

            sI += 1

        return gI
