from typing import List

class MyStack:
    def __init__(self):
        self.q1: List[int] = []
        self.q2: List[int] = []
    def push(self, x: int) -> None:
        self.q2.append(x)
        while self.q1:
            self.q2.append(self.q1.pop(0))
        self.q1, self.q2 = self.q2, []
    def pop(self) -> int:
        return self.q1.pop(0)
    def top(self) -> int:
        return self.q1[0]
    def empty(self) -> bool:
        return not self.q1