from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        self.random_gen = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:

        rands = []
        for i in range(5):
            rand = int(next(self.random_gen))
            rands.append(rand >> 16)

        new_num = ''
        for i in range(16):
            counter = 0
            for i in range(len(rands)):
                if rands[i] % 2 == 1:
                    counter += 1
                rands[i] = rands[i] >> 1
            if counter >= 3:
                new_num = str(1) + new_num
            else:
                new_num = str(0) + new_num

        new_num = int(new_num, base=2)
        new_num = (new_num % k) + 1

        return new_num


if __name__ == "__main__":
    Random_gen = lcg(pow(2, 32), 134775813, 1, 0)
    r = RandomGen()
    r.randint(100)
    r.randint(100)
