class TwoSum:
    def __init__(self):
        self.nums = {}

    def add(self, number: int) -> None:
        self.nums[number] = self.nums.get(number, 0) + 1

    def find(self, value: int) -> bool:
        for num in self.nums:
            complement = value - num

            if complement in self.nums:
                if complement != num or self.nums[num] > 1:
                    return True

        return False
