// https://leetcode.com/problems/intersection-of-two-arrays/description/
// Intersection of two element
#include<bits/stdc++.h>
using namespace std;

int main(){
    int n , m; cin >> n >>m;
    vector<int> a(n) , b(m);
    for(int i = 0 ;i < n;i++) cin >> a[i];
    for(int i = 0 ;i < m;i++) cin >> b[i];
    vector<int> ans;
    unordered_map<int,int> mp;
    for(auto it : a){
        mp[it] = 1;
    }

    for(auto it : b){
        if(mp[it] == 1){
            ans.push_back(it);
        }
    }

    for(auto it : ans){
        cout << it << " ";
    }
}