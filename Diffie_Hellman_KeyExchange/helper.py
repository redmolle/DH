import prime
import random
from math import gcd as bltin_gcd


def is_prime(n):
    return prime.is_prime(n, 128)


def get_prime(length):
    return prime.generate_prime_number(length)


def get_rand_prim(n):
    prim = prim_roots(n)
    return prim[random.randint(0, len(prim))]


def phi(n):
    p = n
    i = 2
    while i * i <= n:
        while n % i == 0:
            n = n / i
            p = - p / i
        if n > 1:
            p = - p / n
        i = i + 1
    return p


def mod(base, exp, modulo):
    return pow(base, exp, modulo)


def prim_roots(modulo):
    required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo) }
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]



