#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

bool check_correct(char input[8]) {
    bool found_increasing = false;
    bool found_prohibited = false;
    bool found_pairs = false;

    char prev_prev = -5;
    char prev = -4;
    char prev_pair = -5;
    for (int idx = 0; idx < 8; idx++) {
        if ( (prev_prev + 2) == (prev + 1) && (prev + 1) == input[idx] ) {
            found_increasing = true;
        }
        if ( prev == input[idx] && prev != prev_pair ) {
            if (prev_pair > 0) {
                found_pairs = true;
            } else {
                prev_pair = prev;
            }
        }

        switch (input[idx]) {
            case 'i':
            case 'o':
            case 'l':
                found_prohibited = true;
                break;
        }

        prev_prev = prev;
        prev = input[idx];
    }

    return found_increasing && found_pairs && (!found_prohibited);
};

void inc_password(char input[8]) {
    for (int offset = 0; offset < 8; offset++) {
        int idx = 7 - offset;
        input[idx]++;
        if (input[idx] <= 'z') {
            return;
        }

        input[idx] = 'a';
    }
}

void inc_until_valid(char input[9]) {
    for (int idx = 0; idx < 16777216; idx++) {
        inc_password(input);
        bool is_correct = check_correct(input);
        if (is_correct) {
            break;
        }
    }
}

int main(int argc, char** argv) {
    if(check_correct("hijklmmn")) {
        printf("hijklmmn >> expected false\n");
        exit(1);
    }
    if(check_correct("abbceffg")) {
        printf("abbceffg >> expected false\n");
        exit(1);
    }
    if(check_correct("abbcegjk")) {
        printf("abbcegjk >> expected false\n");
        exit(1);
    }
    if(!check_correct("abcdffaa")) {
        printf("abcdffaa >> expected true\n");
        exit(1);
    }

    char example1[9] = "abcdefgh\0";
    inc_until_valid(example1);
    printf(">>> abcdefgh next %s\n", example1);

    char example2[9] = "ghijklmn\0";
    inc_until_valid(example2);
    printf(">>> ghijklmn next %s\n", example2);

    char part1[9] = "vzbxkghb\0";
    inc_until_valid(part1);
    printf(">>> part1 next %s\n", part1);

    inc_until_valid(part1);
    printf(">>> part2 next %s\n", part1);
};