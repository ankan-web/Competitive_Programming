from typing import List

class TwoSum:
    def __init__(self):
        self.nums = []
        self.set = set()
    def add(self, number: int) -> None:
        self.nums.append(number)
        self.set.add(number)
    def find(self, value: int) -> bool:
        for num in self.nums:
            if value - num in self.set and (value - num != num or self.nums.count(num) > 1):
                return True
        return False