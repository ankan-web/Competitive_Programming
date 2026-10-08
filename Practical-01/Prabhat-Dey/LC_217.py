#217. Contains Duplicate

class Solution(object):
    def containsDuplicate(self, nums):
        freq = {}
        for i in nums:
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1
        for i in freq:
            if freq[i] > 1:
                return True
        return False