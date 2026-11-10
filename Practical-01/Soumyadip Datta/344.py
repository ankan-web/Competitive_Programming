class Solution(object):
    def reverseString(self, s):
        l=len(s)
        
        for i in range(l//2):
            s[i],s[l-i-1]=s[l-i-1],s[i]
        
        return s
