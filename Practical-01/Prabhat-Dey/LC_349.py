#349. Intersection of Two Arrays

class Solution(object):
    def intersection(self, nums1, nums2):
        a=set(nums1)
        b=set(nums2) 
        r=list(a&b)
        return r     