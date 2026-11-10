class Solution(object):
    def firstUniqChar(self, s):
        n = len(s)
        c = {}
        for i in s:
            if i in c:
                c[i] = c[i] + 1
            else:
                c[i] = 1
        for i in range(n):
            if c[s[i]] == 1:
                return i
        return -1