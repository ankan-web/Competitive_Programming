class Solution:
    def isValid(self, s: str) -> bool:

        stk = []
        order = {"]": "[", ")": "(", "}": "{"}

        for i in s:
            if i in order:
                if not stk or stk.pop() != order[i]:
                    return False

            else:
                stk.append(i)

        return len(stk) == 0
