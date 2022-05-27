from __future__ import annotations
# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from random_gen import RandomGen

class Game:
    
    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        # Potion Hash Table (Contains all possible potions)
        self.potion_table = LinearProbePotionTable(3)
        # Potion Binary Search Tree (Contains potions that are purchasable)
        self.potion_inventory = AVLTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        # Initialise the Hash Table
        # Time complexity should be O(len(potion_data)* insert) = O(C), where C is the length of potion_data
        self.potion_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            # Add all the potions and hash the name of each potion
            self.potion_table[potion[0]] = potion

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        # Adds the potions that are being sold to AVL Tree
        # Time Complexity should be O(len(potion_name_amount_pairs) * comp(insert))
        # Time Complexity will be O(C * log(N)) since inserting into an AVL Tree will rebalance the tree when unbalanced
        # , this guarantees the insertion to be log(N).
        for potion in potion_name_amount_pairs:
            potion_price = self.potion_table[potion[0]][2]
            self.potion_inventory[potion_price] = potion

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        # Overall complexity of O(C*(log(N) + log(N) + append) = O(C*log(N))
        # Initialise the potions that are being sold
        potion_sell_list = []
        # For every vendor, pick a random kth-largest potion
        for i in range(num_vendors):
            # Choose a random number between 0 and C - i, where C is the number of potions and i is the ith vendor
            number_to_choose = len(self.potion_inventory) - i
            # Select a random number between 0 to C - i
            p = RandomGen().randint(number_to_choose)
            # Get the potion: O(log(N))
            potion = self.potion_inventory.kth_largest(p)
            # Append the potion: O(append)
            potion_sell_list.append(potion.item)
            # Delete the potion: O(log(N))
            self.potion_inventory.__delitem__(potion.key)
        return potion_sell_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        raise NotImplementedError()


G = Game()
# Setting the potions with the stats: Name, Category, Buying Price from Vendors ($/L)
G.set_total_potion_data([
["Potion of Health Regeneration", "Health", 20],
["Potion of Extreme Speed", "Buff", 10],
["Potion of Deadly Poison", "Damage", 45],
["Potion of Instant Health", "Health", 5],
["Potion of Increased Stamina", "Buff", 25],
["Potion of Untenable Odour", "Damage", 1]
])

G.add_potions_to_inventory([
    ("Potion of Health Regeneration", 4),
    ("Potion of Extreme Speed", 5),
    ("Potion of Instant Health", 3),
    ("Potion of Increased Stamina", 10),
    ("Potion of Untenable Odour", 5)
])

selling = G.choose_potions_for_vendors(4)
print(selling)