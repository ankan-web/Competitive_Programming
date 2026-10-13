#include <stdlib.h>

int compareFrequency(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;

    extern int freq1636[2001];

    int fx = freq1636[x + 1000];
    int fy = freq1636[y + 1000];

    if (fx != fy) {
        return fx - fy;
    }

    return (y > x) - (y < x);
}

int freq1636[2001];

int* frequencySort(int* nums, int numsSize,
                   int* returnSize) {
    for (int i = 0; i < 2001; i++) {
        freq1636[i] = 0;
    }

    for (int i = 0; i < numsSize; i++) {
        freq1636[nums[i] + 1000]++;
    }

    int* result = malloc(numsSize * sizeof(int));

    if (result == NULL) {
        *returnSize = 0;
        return NULL;
    }

    for (int i = 0; i < numsSize; i++) {
        result[i] = nums[i];
    }

    qsort(result, numsSize, sizeof(int), compareFrequency);

    *returnSize = numsSize;
    return result;
}
