from typing import List

class Solution:
    def assignCookies(self, children: List[int], cookies: List[int]) -> int:
        children.sort()
        cookies.sort()
        i = j = result = 0
        while i < len(children) and j < len(cookies):
            if cookies[j] >= children[i]:
                result += 1
                i += 1
                j += 1
            else:
                j += 1
        return result