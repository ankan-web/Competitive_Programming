from collections import Counter


class Solution:
    def firstUniqChar(self, s: str) -> int:

        alphacount = Counter(s)

        for k, v in alphacount.items():
            if v == 1:
                return s.index(k)

        return -1
