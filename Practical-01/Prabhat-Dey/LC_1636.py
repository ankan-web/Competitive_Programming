#1636. Sort Array by Increasing Frequency

class Solution(object):
    def frequencySort(self, nums):
        freq = {}
        for i in nums:
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1
        arr = list(freq.keys())
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if freq[arr[i]] > freq[arr[j]]:
                    arr[i], arr[j] = arr[j], arr[i]
                elif freq[arr[i]] == freq[arr[j]] and arr[i] < arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
        ans = []
        for i in arr:
            for j in range(freq[i]):
                ans.append(i)
        return ans
        