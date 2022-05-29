""" Game

Runs the game, which handles potion inventory of PotionCorp and vendors. Finds the optimum profit for a given starting
money value
"""
from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Jackson Goerner, Ze Chong, Daniel Ding and Maily Butel'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from linked_stack import LinkedStack
from potion import Potion
from random_gen import RandomGen


class Game:
    """
        The Game class contains all the functionality to set all potion data, add potions
        to PotionCorp's inventory, assign potions to vendors and calculate the maximum money
        that can be made given a starting allowance.

        To store potion data, the LinearProbePotionTable data type has been implemented.
        This use of hashing and linear probing allows for constant time access and insertion of Potions.

        Since a vendor must be able to choose a kth most expensive potion from the inventory,
        the potions in the inventory must be stored in sorted order. Because they always remain sorted
        and balanced, AVL trees are able to insert, delete and find the kth most expensive potion
        in logarithmic time. Thus, it is the chosen data type.

        To calculate the maximum money to be made per day, Stack and AVL tree data types have been implemented.
        The AVL tree allows for the calculated trades to be stored in sorted order efficiently since insertion
        is logarithmic time. The Stack data type allows for quick constant time access to the next trade the
        player should make.
    """

    def __init__(self, seed=0) -> None:
        """
        Game initialiser
        :param seed: the seed use for the random generator
        """
        self.rand = RandomGen(seed=seed)
        # Potion Hash Table (Contains all possible potions)
        self.potion_table = LinearProbePotionTable(100)
        # Potion Binary Search Tree (Contains potions that are purchasable)
        self.potion_inventory = AVLTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Initialises the Hash Table. Uses the hash_table ADT so that accessing potions can be done in constant time
        given that the name of the potion is known. This also enables inserting potions to be in constant time.

        :complexity: O(len(potion_data)* insert) = O(C), where C is the length of potion_data list
        O(insert) is assumed to be in constant time
        :param potion_data: list containing values that describe the potion -> [Type, Name, Buying Price]
        :return: None
        """

        self.potion_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            # Add all the potions and hash the name of each potion
            self.potion_table[potion[1]] = Potion.create_empty(potion[0], potion[1], potion[2])

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds the potion tuples that are being sold to AVL Tree. Since AVL trees remain sorted and balanced,
        insertion, searches and deletion can be performed with logarithmic complexity.

        :complexity: O(C * log(N))
        where C is the length of potion_name_amount_pairs
              N is the number of potions provided in set_total_potion_data

        The complexity for this method is given by O(C * insert) since it always iterates through each item in
        potion_name_amount_pairs and inserts each potion into the inventory.
        The inventory is constructed using an AVL tree as described above, so insert complexity is log(N).
        Thus, overall complexity is O(C * log(N))

        :param potion_name_amount_pairs: List of elements containing a tuple of (Name, Amount of Potion in Litres)
        :return: None
        """

        for potion in potion_name_amount_pairs:
            potion_price = self.potion_table[potion[0]].buy_price
            self.potion_inventory[potion_price] = potion

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Chooses the potions that each vendor will offer based on the random number generator and returns them as a list.
        Uses the random_gen file to generate random numbers.

        :complexity: O(C * log(N))
        where C is num_vendors
              N is number of potions provided in set_total_potion_data

        Since this method always iterates through each integer in the range of num_vendors and for each iteration
        it deletes and finds the kth most expensive potion from inventory and adds it to a list, the complexity
        is given by O(C*(kth_largest + delete + append)).
        The AVL tree used to store the inventory allows for deletion in log(N) complexity and finding the kth
        most expensive potion too.
        see AVLTree kth_largest_aux(self, k: int, current: AVLTreeNode) -> AVLTreeNode
        Appending a potion to the end of potion_sell_list is done in constant time.
        Therefore, O(C*(kth_largest + delete + append)) = O(C*(log(N) + log(N) + 1)) = O(C*log(N))

        :param num_vendors: Number of vendors
        :return: list of selling potions
        """

        potion_sell_list = []
        # For every vendor, pick a random kth-largest potion
        for i in range(num_vendors):
            # Choose a random number between 0 and the number of potions remaining in the inventory
            number_to_choose = len(self.potion_inventory)
            # Select a random number between 0 to the number of potions remaining in the inventory
            p = self.rand.randint(number_to_choose)
            # Get the potion from inventory: O(log(N))
            potion = self.potion_inventory.kth_largest(p)
            # Append the potion to list: O(append)
            potion_sell_list.append(potion.item)
            # Delete the potion from inventory: O(log(N))
            del self.potion_inventory[potion.key]

        # put all potions back into inventory
        self.add_potions_to_inventory(potion_sell_list)

        return potion_sell_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[float]) -> list[float]:
        """
        Method to try and find the optimal profit for a given starting money value.

        ----------------------------------------------------------------------------------------------------------
        This solution consists of two main sections: Determining and storing possible trades sorted by profit, and
        calculating how much the player can make per day.

        1) An AVL tree is used to store the possible trades since it inserts in logarithmic time and maintains them
        in sorted order.
        The corresponding potion in potion_table is found for each potion in potion_valuations.
        The profit made per dollar spent is calculated.
        This is done as opposed to profit per litre since it takes into account of how many litres can be bought and
        sold during the trade.

        For example,
        Potion 1: costs $3/L, sells for $5/L so profit/L is $2/L
        Potion 2: costs $1/L, sells for $2/L so profit/L is $1/L
        If player has $6 starting money, they can buy 2L of Potion 1 or 6L of Potion 2 (infinite supply assumed)
        Potion 1 money made = 2L * $2/L = $4
        Potion 2 money made = 6L * $1/L = $6
        So, the profit stored in the AVL Tree is    (sell price - buy price)/buy price
        The maximum amount made from the trade is also needed, so it is stored with profit in the AVL tree.

        2) Each day the possible trades are stored into a Stack data type since it allows quick access to the most
        profitable trade. The player spends as much money as they can on the current most profitable trade and when
        their money is out, that day is over.
        ----------------------------------------------------------------------------------------------------------

        :complexity: O(N * log(N) + M * N)
        where N is the length of potion_valuations
              M is the length of starting_money

        Since the first section of the solution iterates through potion_valuations and gets the data from the
        hash table, accesses the potion from the inventory, checks if the trade is in the trades AVL tree, and
        possibly deletes the trade from the AVL tree, it has complexity
        O(N * (access hash + access tree + contains + delete)) = O(N * (1 + log(N) + log(N) + log(N)))
         = O(N * log(N))

        The second section always iterates through stating_money and for each iteration puts all trades into
        a stack and pops each item off the stack one by one to complete calculations. Therefore, it has complexity
        O(M * (tree traversal + put items in stack + go through stack))
        The tree traversal always passes through each link twice, so it has complexity O(2N)
        pushing and popping every trade into/out of the stack has complexity O(N) each since it visits each element.
        So, O(M * (tree traversal + put items in stack + go through stack)) = O(M * (2N + N + N))
            = O(M * N)

        All together, the complexity is O(section1 + section2) = O(N * log(N) + M * N)

        ----------------------------------------------------------------------------------------------------------

        :param potion_valuations: list of potion names and the buying price of adventurers
        :param starting_money: list of starting money values
        :return: list of optimal profit for each starting money value
        """
        results = []
        profits_tree = AVLTree()

        # iterate through each potion
        for potion in potion_valuations:
            # get the potion data from potion data hash table
            potion_vendor_price = self.potion_table[potion[0]].buy_price
            # To get optimal trades, base them on how much you can earn per dollar spent
            # So, possible trades will be stored in AVLTree based on profit_per_dollar
            # This is done by ($(sell)/L - $(spend)/L) / $(spend)/L
            #                = ∂$/L / $(spend)/L    => or ∂$/L * L/$(spend)
            #                = ∂$/$(spend)     "the money earned per dollar spent"
            litres_available = self.potion_inventory[potion_vendor_price][1]
            profit_per_litre = potion[1] - potion_vendor_price
            profit_per_dollar = profit_per_litre / potion_vendor_price
            # Must have a limit to each trade. Instead of basing it on Litres, convert
            # this to maximum money spent per trade
            max_money_spend = litres_available * potion_vendor_price

            # Only add in positive profits
            if profit_per_dollar > 0:
                # BST can only have unique nodes. So, if two potions have the same profit per dollar, sum them
                # This can be done since they are now essentially the same
                if profit_per_dollar in profits_tree:
                    previous_max_money_spend = profits_tree[profit_per_dollar][1]
                    del profits_tree[profit_per_dollar]
                    profits_tree[profit_per_dollar] = [profit_per_dollar, max_money_spend + previous_max_money_spend]
                else:
                    profits_tree[profit_per_dollar] = [profit_per_dollar, max_money_spend]

        # Play each day                         # O(M * (N + N)) = O(M * N)
        for i in range(len(starting_money)):  # O(M)
            # iterate through AVL Tree inorder and put in Stack
            profits_stack = LinkedStack()
            iterable = iter(profits_tree)
            for j in range(len(profits_tree)):  # O(N) since each link is passed twice
                profits_stack.push(next(iterable))

            player_money = starting_money[i]
            # earnings always starts with the money we start with
            earnings = player_money

            # start from top of stack (most profitable), going down
            for k in range(len(profits_stack)):  # O(N)
                trade = profits_stack.pop()  # O(1)

                # if the player doesn't have enough for the whole trade,
                # do their maximum and finish the day
                if player_money <= trade[1]:
                    earnings += player_money * trade[0]
                    break

                # They can do the whole trade. Then move on to the next best one
                else:
                    earnings += trade[0] * trade[1]
                    player_money = player_money - trade[1]
            results.append(earnings)
        return results
