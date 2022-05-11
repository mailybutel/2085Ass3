import math


def largest_prime(k: int) -> int:
    """ Put this in my own words: This algorithm produces all primes not greater than n.
    It includes a common optimization, which is to start enumerating the multiples of each prime i from i2.
    The time complexity of this algorithm is O(n log log n),[8] provided the array update is an O(1) operation,
    as is usually the case. """
    is_prime = [True for i in range(2, k)]

    for i in range(2, int(math.sqrt(k))):
        if is_prime[i-2]:
            for j in range(i**2, k, i):
                is_prime[j-2] = False

    largest_prime = 2

    for i in range(len(is_prime)-1, -1, -1):
        if is_prime[i]:
            return i+2

    return largest_prime
