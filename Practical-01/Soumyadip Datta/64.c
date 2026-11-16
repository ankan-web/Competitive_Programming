int minPathSum(int** grid, int gridSize, int* gridColSize) {
    int m = gridSize;          
    int n = gridColSize[0];   

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) {
                continue;                         
            }
            else if (i == 0) {
                grid[i][j] += grid[i][j-1];        
            }
            else if (j == 0) {
                grid[i][j] += grid[i-1][j];        
            }
            else {
                int up = grid[i-1][j];
                int left = grid[i][j-1];
                grid[i][j] += (up < left) ? up : left;
            }
        }
    }
    return grid[m-1][n-1];
}