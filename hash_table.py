""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner, Ze Chong, Daniel Ding and Maily Butel'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

from potion import Potion
from primes import largest_prime
from referential_array import ArrayR
from typing import TypeVar, Generic
T = TypeVar('T')


class LinearProbePotionTable(Generic[T]):
    """
    Linear Probe Potion Table

    This potion table does not support deletion.

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        table_size: current size of the hash table
    """

    def __init__(self, max_potions: int, good_hash: bool=True, tablesize_override: int=-1) -> None:
        # Statistic setting
        self.conflict_count = 0
        self.probe_max = 0
        self.probe_total = 0
        self.hash_choice = good_hash
        if tablesize_override == -1:
            self.initalise_with_tablesize(largest_prime(max_potions * 2))
        else:
            self.initalise_with_tablesize(tablesize_override)

    def hash(self, potion_name: str) -> int:
        """
        Hashes a string based on the choice of hash function
        :param potion_name: name of potion as a string
        :return: integer
        """

        if self.hash_choice:
            # Good Hash Function
            return Potion.good_hash(potion_name, self.table_size)
        else:
            # Bad Hash Function
            return Potion.bad_hash(potion_name, self.table_size)

    def statistics(self) -> tuple:
        """
        Good Hash Function:
        Good hash function takes the ASCII value of each character in the string and uses noise values to create a
        pseudo random value. Since the hash table always has double the space of the inputs, there is a random and
        low chance of conflicts. Therefore, conflict count does not increase as table size increases.

        The longest probe length will also be random since the input string will hash a random value, probe chains
        are expected to be less than the bad hash function and will not increase as the table size increases.

        The total probe distance depends on the number of conflicts and the longest probe chain, however since neither
        of those are dependent on the table size, the total distance probed will also not depend on the table size.


        Bad Hash Function:
        Bad hash function takes the ascii value of the first character in the string and finds the modulo of that with
        the table size. Therefore, once all the ascii values have been taken, there will be a linear increase in amount
        of conflicts as the table size increases.

        The longest probe length will also increase linearly after a certain table size. Once all the ASCII values are
        taken, conflicts will start to appear and the longest probe length will be the number of ASCII values taken
        plus the number of conflicts.

        The total distance probed will increase exponentially however since every time a conflict is added, the probe
        length of the chain will increase to chain length + 1 and will run through that every conflict.

        :return: a tuple of (number of conflicts, total distance probed, length of longest probe chain)
        """
        return (self.conflict_count, self.probe_total, self.probe_max)
         

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self.count

    def __linear_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing
        :complexity best: O(K) first position is empty
                          where K is the size of the key
        :complexity worst: O(K + N) when we've searched the entire table
                           where N is the table_size
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)

        checked = True
        probe = []

        for _ in range(len(self.table)):  # start traversing
            if self.probe_max < len(probe):
                self.probe_max = len(probe)
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                if checked:
                    self.conflict_count += 1
                    checked = False
                probe.append(position)
                self.probe_total += 1

                position = (position + 1) % len(self.table)

        raise KeyError(key)
        
    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist
        """
        position = self.__linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set an (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__contains__(key: str)
        """
        if len(self) == len(self.table) and key not in self:
            raise ValueError("Cannot insert into a full table.")
        position = self.__linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)

    def initalise_with_tablesize(self, tablesize: int) -> None:
        """
        Initialise a new array, with table size given by tablesize.
        Complexity: O(n), where n is len(tablesize)
        """
        self.count = 0
        self.table_size = tablesize
        self.table = ArrayR(tablesize)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
