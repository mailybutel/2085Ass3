"""
    Defines a Potion to be used in the game
"""
__author__ = 'Ze Chong, Daniel Ding and Maily Butel'

from primes import largest_prime


class Potion:
    """
        Potion class that represents a potion that can be bought or sold
    """
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        """
            Potion initialiser
            :complexity: O(1)
        """
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
            Creates a potion with 0 quantity
            :complexity: O(1)
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
            A good hash function results in few collisions
            :complexity: O(n) where n is the length of the potion's name
        """
        value = 0
        noise = largest_prime(1000)
        hash_base = largest_prime(5000)
        for char in potion_name:
            value = (ord(char) + value*noise) % tablesize
            noise = (noise * hash_base) % (tablesize - 1) # changes for each position pseudo randomly
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
            A bad hash function that results in many collisions
            :complexity: O(comp(ord))
        """
        return ord(potion_name[0]) % tablesize

