from primes import largest_prime


class Potion:
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """"""
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        value = 0
        noise = largest_prime(1000)
        hash_base = largest_prime(5000)
        for char in potion_name:
            value = (ord(char) + value + noise) % tablesize
            noise = (noise * hash_base) % (tablesize - 1)
        return value
    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        return ord(potion_name[0]) % tablesize

