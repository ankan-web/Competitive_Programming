class Solution(object):
    def rob(self, nums):
        p1=0
        p2=0
        for i in nums:
            current_val=max(p1,p2+i)
            p2,p1=p1,current_val
        return current_val