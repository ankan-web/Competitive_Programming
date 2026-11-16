from collections import Counter, defaultdict


class Solution:
    def frequencySort(self, nums: list[int]) -> list[int]:

        freq = Counter(nums)
        sot = defaultdict(list)

        for k, v in sorted(freq.items(), reverse=True):
            sot[v].extend([k] * v)

        lst = []

        for key in sorted(sot.keys()):
            lst.extend(sot[key])

        return lst
