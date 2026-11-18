from typing import List

class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        # Count frequencies
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        # Sort by frequency ascending, then by value descending
        nums.sort(key=lambda x: (freq[x], -x))
        return nums