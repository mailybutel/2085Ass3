""" Generates a random number. """

__author__ = 'Ze Chong, Daniel Ding and Maily Butel'

from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:
    """
        Random number generator.
    """

    def __init__(self, seed: int = 0) -> None:
        """
            Random number generator initialiser
            :complexity: O(1)
        """
        # random_gen is the Generator returned from lcg
        # used to get each random number of randint
        self.random_gen = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        Generates a new random number less than k.

        :complexity: O(1) for best and worst case since it always generates 5 random numbers
            and iterates through their 16 most significant bits. Does not depend on value of k.
        """

        # Get 5 random values and store then in an array
        rands = []
        for i in range(5):
            rand = int(next(self.random_gen))
            # remove 16 least significant bits
            rands.append(rand >> 16)

        # Compare each bit in the 5 random numbers and store the result in a string
        new_num = ''
        for i in range(16):
            # counter keeps track of how many of the 5 random numbers have a 1 in the current bit
            counter = 0
            for i in range(len(rands)):
                # Divide by 2 to check if 0 or 1 and increment counter if 1.
                if rands[i] % 2 == 1:
                    counter += 1
                # Right shift to remove last bit
                rands[i] = rands[i] >> 1
            # update string based on counter
            if counter >= 3:
                new_num = str(1) + new_num
            else:
                new_num = str(0) + new_num

        # convert string to int and return it modulo k + 1
        new_num = int(new_num, base=2)
        new_num = (new_num % k) + 1

        return new_num


if __name__ == "__main__":
    Random_gen = lcg(pow(2, 32), 134775813, 1, 0)
    r = RandomGen()
    r.randint(100)
    r.randint(100)
