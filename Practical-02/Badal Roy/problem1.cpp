// https://leetcode.com/problems/number-of-1-bits/description/
// Number of 1 Bit

#include<bits/stdc++.h>
using namespace std;

int main(){
    int n; cin >> n;
    int count = 0;
    while(n){
        if(n&1) count++;
        n >>= 1;
    }
    cout << count << endl;
}