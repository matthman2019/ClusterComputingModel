#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>
#include <stdbool.h>
#include <assert.h>
#include <string.h>


bool is_mersenne_prime(char* input_number) {
    mpz_t mersenne_number;
    mpz_t s;
    mpz_t two;
    int input_number_int = atoi(input_number);

    mpz_init(mersenne_number);
    mpz_set_ui(mersenne_number, 0);
    mpz_init(s);
    mpz_set_ui(s, 4);
    mpz_init(two);
    mpz_set_ui(two, 2);

    mpz_ui_pow_ui(mersenne_number, 2, input_number_int);
    mpz_sub_ui(mersenne_number, mersenne_number, 1);

    int i;
    for (i = 0; i < input_number_int-2; i++) {
        mpz_mul(s, s, s); // square s
        mpz_sub_ui(s, s, 2); // subtract 2
        mpz_mod(s, s, mersenne_number);
    }
    return (mpz_cmp_ui(s, 0) == 0);
}

int main() {
    return 0;
}
