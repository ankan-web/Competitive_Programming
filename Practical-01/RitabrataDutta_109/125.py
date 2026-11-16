class Solution:
    def isPalindrome(self, s: str) -> bool:

        if s == " " or len(s) == 1:
            return True

        result = "".join(char.lower() for char in s if char.isalnum())

        n = len(result)

        if n == 0:
            return True

        for i, j in zip(range(0, n), range(n - 1, -1, -1)):
            if i == j or (i + 1) == j:
                if result[i] == result[j]:
                    return True
                else:
                    return False
            else:
                if result[i] != result[j]:
                    return False
