#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <immintrin.h>

int find_drop_time(int* ps, int* sz, int count) {
    int* target_pos = (int*) malloc( count * sizeof(int) );
    int* pos = (int*) malloc( count * sizeof(int) );
    
    // 4 :: 0 1 2 3
    // [7]
    int time = 0;
    for (int idx = 0; idx < count; idx++) {
        time++;
        pos[idx] = ps[idx];
        target_pos[idx] = sz[idx] - (time % sz[idx]);
        target_pos[idx] %= sz[idx];
    }

    time = 0;
    int max_delta = -1;
    while (max_delta != 0) {
        max_delta = 0;

        for (int idx = 0; idx < count; idx++) {
            int delta = target_pos[idx] - pos[idx];
            if (delta < 0) {
                delta += sz[idx];
            }
            if (max_delta < delta) {
                max_delta = delta;
            }
        }

        for (int idx = 0; idx < count; idx++) {
            pos[idx] = (pos[idx] + max_delta) % sz[idx];
        }

        time += max_delta;
    }

    free(pos);
    free(target_pos);
    return time;
}

static inline uint64_t get_time_counter() {
    return __rdtsc();
}

int main(int argc, char** argv) {
    //int ps[2] = { 4, 1 };
    //int sz[2] = { 5, 2 };

    // part1
    // int ps[6] = { 2 , 7  , 10 , 2 , 9  , 0 };
    // int sz[6] = { 5 , 13 , 17 , 3 , 19 , 7 };

    // part2
    int ps[7] = { 2 , 7  , 10 , 2 , 9  , 0,  0 };
    int sz[7] = { 5 , 13 , 17 , 3 , 19 , 7, 11 };

    int drop_time = find_drop_time(ps, sz, 7);

    printf("drop time part: %d\n", drop_time);

    // partX performance test
    uint64_t best_time = INT64_MAX;
    for (int r = 0; r < 100; r++) {
        uint64_t start = get_time_counter();
        drop_time = find_drop_time(ps, sz, 7);
        uint64_t stop = get_time_counter();
        uint64_t delta = stop - start;
        if (best_time > delta) {
            best_time = delta;
        }
    }

    printf("perf: %d -- best time: %lu\n", drop_time, best_time);
}
