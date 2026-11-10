
class Solution(object):
    def isPalindrome(self, s):
        st=s.lower()
        n=""
        for i in st:
            if i.isalnum():
                n=n+i

        if n==n[::-1]:
            return True
        else:
            return False