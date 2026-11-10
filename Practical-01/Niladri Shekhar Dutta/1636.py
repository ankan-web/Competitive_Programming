class Solution:
    def frequencySort(self, nums: list[int]) -> list[int]:
        freq = Counter(nums)

        nums.sort(key=lambda x: (freq[x], -x))

        return nums