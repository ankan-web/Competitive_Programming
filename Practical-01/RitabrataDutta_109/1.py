class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
        unordered_map<int, int> indexMap;
        int n = nums.size();

        for(int i = 0; i < n; i++){
            indexMap[nums[i]] = i;
        }

        for(int i = 0; i < n; i++){
            int left = target - nums[i];
            if (indexMap.find(left) != indexMap.end() && indexMap[left]!=i){
                return {i, indexMap[left]};
            }
        }

        return {};

    }
};
