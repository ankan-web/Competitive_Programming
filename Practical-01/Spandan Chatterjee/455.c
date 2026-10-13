#include <stdlib.h>

int compareCookies(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;

    return (x > y) - (x < y);
}

int findContentChildren(int* g, int gSize,
                        int* s, int sSize) {
    qsort(g, gSize, sizeof(int), compareCookies);
    qsort(s, sSize, sizeof(int), compareCookies);

    int child = 0;
    int cookie = 0;

    while (child < gSize && cookie < sSize) {
        if (s[cookie] >= g[child]) {
            child++;
        }

        cookie++;
    }

    return child;
}
