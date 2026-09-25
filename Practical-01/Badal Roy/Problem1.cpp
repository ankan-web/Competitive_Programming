// https://leetcode.com/problems/contains-duplicate/description/
// contain duplicate

#include<bits/stdc++.h>
using namespace std;

int main(){
    int n; cin >> n;
    vector<int> a(n);
    unordered_set<int> s;
    for(int i = 0 ;i <n;i++)cin >> a[i];
    bool c = false;
    for(auto it : a){
        if(s.count(it) > 0){
            c = true;
            break;
        }

        s.insert(it);
    }

    if(c){
        cout << "Duplicate present" << endl;
    }
    else{
        cout << "Duplicate not present" << endl;
    }
    
 }