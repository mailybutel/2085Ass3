""" This module is used to find prime numbers. """

__author__ = 'Ze Chong, Daniel Ding and Maily Butel'

import math


def largest_prime(k: int) -> int:
    """
    Finds the largest prime number less than k.
    :pre: k > 2
    :complexity: O(n log log n)
    """

    # 2 is the smallest prime number so k must be >2
    if k <= 2:
        raise ValueError("Integer must be greater than 1")

    # array of boolean values to keep track of primes
    # 0 = not prime, 1 = prime
    is_prime = [True for i in range(k)]

    # 0 and 1 are not primes
    is_prime[0] = False
    is_prime[1] = False

    # go through the array until the square root of k
    for i in range(int(math.sqrt(k))):
        # If the element is a prime, turn off all multiples of it
        if is_prime[i]:
            for j in range(i ** 2, k, i):
                is_prime[j] = False

    # Go backwards through the array and return the first prime found.
    for i in range(len(is_prime) - 1, -1, -1):
        if is_prime[i]:
            return i
