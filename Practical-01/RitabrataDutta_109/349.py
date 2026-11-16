class Solution:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:

        num1 = set(nums1)
        result = set()

        for i in nums2:
            if i in num1:
                result.add(i)
        return list(result)
