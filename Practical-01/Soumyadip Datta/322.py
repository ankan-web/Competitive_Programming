int coinChange(int* coins, int coinsSize, int amount){
    int dp[amount + 1];
    for(int a = 0; a <= amount; a++)
        dp[a] = amount + 1;          // "infinity"
    dp[0] = 0;

    for(int a = 1; a <= amount; a++){
        for(int k = 0; k < coinsSize; k++){
            if(coins[k] <= a && dp[a - coins[k]] + 1 < dp[a])
                dp[a] = dp[a - coins[k]] + 1;
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}