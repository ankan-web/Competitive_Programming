from typing import List

class Solution:
    def backspaceCompare(self, S: str, T: str) -> bool:
        def build(s: str) -> List[str]:
            stack = []
            for ch in s:
                if ch != '#':
                    stack.append(ch)
                elif stack:
                    stack.pop()
            return stack
        return build(S) == build(T)