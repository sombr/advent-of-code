#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <omp.h>

struct State {
    unsigned long long reg[3];
    char ip;
    char op;
};

struct State new_state(unsigned long long areg) {
    struct State res;
    res.ip = 0;
    res.op = 0;
    res.reg[0] = areg;
    res.reg[1] = 0;
    res.reg[2] = 0;

    return res;
}

typedef bool (*operation)(struct State *state, long operand, char *out);

static inline unsigned long long process_combo(struct State *state, long op) {
    if (op >= 0 && op < 4) {
        return op;
    }
    if (op == 7) {
        exit(7);
    }
    return state->reg[ op - 4 ];
}

static inline unsigned long long Xdv(struct State *state, long operand) {
    unsigned long long numerator = state->reg[0];
    unsigned long long denominator = 1 << process_combo(state, operand);

    unsigned long long res = numerator / denominator;
    return res;
}

bool adv(struct State *state, long operand, char* out) {
    state->reg[0] = Xdv(state, operand);
    return true;
}

bool bxl(struct State *state, long operand, char* out) {
    state->reg[1] = state->reg[1] ^ operand;
    return true;
}

bool bst(struct State *state, long operand, char *out) {
    state->reg[1] = process_combo(state, operand) % 8;
    return true;
}

bool jnz(struct State *state, long operand, char *out) {
    if (state->reg[0] == 0) {
        return true;
    }
    state->ip = operand;
    return false;
}

bool bxc(struct State *state, long operand, char *out) {
    state->reg[1] = state->reg[1] ^ state->reg[2];
    return true;
}

bool out(struct State *state, long operand, char *out) {
    unsigned long long res = process_combo(state, operand) % 8;
    out[ state->op ] = res;
    state->op = state->op + 1;
    return true;
}

bool bdv(struct State *state, long operand, char *out) {
    state->reg[1] = Xdv(state, operand);
    return true;
}

bool cdv(struct State *state, long operand, char *out) {
    state->reg[2] = Xdv(state, operand);
    return true;
}

bool run_and_check(unsigned long long regA, char* program, char* outs, int psize) {
    operation opmap[] = {
        adv,
        bxl,
        bst,
        jnz,
        bxc,
        out,
        bdv,
        cdv
    };

    struct State state = new_state(regA);

    while (state.ip >= 0 && state.ip < psize) {
        operation op = opmap[ program[state.ip] ];
        bool proceed = op(&state, program[state.ip+1], outs);

        if (op == out) {
            if (state.op > psize || program[state.op-1] != outs[state.op-1]) {
                return false;
            }
        }

        if (proceed) {
            state.ip += 2;
        }
    }

    // comparison
    if (state.op != psize) {
        return false;
    }

    for (int idx = 0; idx < psize; idx++) {
        if (program[idx] != outs[idx]) {
            return false;
        }
    }
    return true;
}

int main(int argc, char** argv) {
    setbuf(stdout, NULL);
    unsigned long long ainit = 1;

    //char program[] = {0,3,5,4,3,0};
    char program[] = {2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0};
    char outs[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

    int psize = sizeof(program) / sizeof(char);
    printf(">> psize: %d\n", psize);

    run_and_check(ainit, program, outs, psize);
    for (int idx = 0; idx < psize; idx++) {
        printf("%s%d", (idx == 0 ? "" : ","), outs[idx]);
    }
    printf("\n");

    #pragma omp parallel for
    for (unsigned long long areg = 35184372088832; areg < 281474976710656; areg++) {
        if (areg % 500000000 == 0) {
            fprintf(stderr, "passing %llu\n", areg);
        }
        if (run_and_check(areg, program, outs, psize)) {
            printf("part2 found at: %llu\n", areg);
        }
    }
    for (int idx = 0; idx < psize; idx++) {
        printf("%s%d", (idx == 0 ? "" : ","), outs[idx]);
    }
    printf("\n");
}
