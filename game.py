""" Game

Runs the game, which handles potion inventory of PotionCorp and vendors. Finds the optimum profit for a given starting
money value
"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner, Ze Chong, Daniel Ding and Maily Butel'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'
from __future__ import annotations
# ^ In case you aren't on Python 3.10
from avl import AVLTree
from hash_table import LinearProbePotionTable
from potion import Potion
from random_gen import RandomGen

class Game:

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        # Potion Hash Table (Contains all possible potions)
        self.potion_table = LinearProbePotionTable(100)
        # Potion Binary Search Tree (Contains potions that are purchasable)
        self.potion_inventory = AVLTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Initialises the Hash Table. Uses the hash_table ADT so that accessing potions can be done in constant time given that
        you have the name of the potion. This also enables inserting and deleting potions to be in constant time.

        Time complexity should be O(len(potion_data)* insert) = O(C), where C is the length of potion_data
        O(insert) is assumed to be in constant time
        :param potion_data: list containing values of [Name, Type, Buying Price]
        :return: None
        """

        self.potion_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            # Add all the potions and hash the name of each potion
            self.potion_table[potion[1]] = Potion.create_empty(potion[0], potion[1], potion[2])

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds the potion tuples that are being sold to AVL Tree. Uses the avl ADT ensures that the potions that are being
        added will be sorted in a tree at logN complexity. Accessing the node and deleting the node will also be
        performed in logN time.

        Time Complexity should be O(len(potion_name_amount_pairs) * insert)
        Time Complexity will be O(C * log(N)) since inserting into an AVL Tree will rebalance the tree when unbalanced
        , this guarantees the insertion to be log(N).
        O(insert) = log(N)
        O(len(potion_name_amount_pairs) = C

        :param potion_name_amount_pairs: List of elements containing a tuple of (Name, Amount of Potion in Litres)
        :return: None
        """

        for potion in potion_name_amount_pairs:
            potion_price = self.potion_table[potion[0]].buy_price
            self.potion_inventory[potion_price] = potion

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Chooses the potions that the vendor will offer based on the random number generator. Uses the random_gen file
        to generate random numbers.

        Overall complexity of O(C*(kth_largest + delete + append)) = O(C*(log(N) + log(N) + append)) = O(C*log(N))
        Initialise the potions that are being sold and returns a list to be sold.

        :param num_vendors: Number of vendors
        :return: list of selling potions
        """

        potion_sell_list = []
        # For every vendor, pick a random kth-largest potion
        for i in range(num_vendors):
            # Choose a random number between 0 and C - i, where C is the number of potions and i is the ith vendor
            number_to_choose = len(self.potion_inventory)
            # Select a random number between 0 to C - i
            p = self.rand.randint(number_to_choose)
            # Get the potion: O(log(N))
            potion = self.potion_inventory.kth_largest(p)
            # Append the potion: O(append)
            potion_sell_list.append(potion.item)
            # Delete the potion: O(log(N))
            self.potion_inventory.__delitem__(potion.key)

        self.add_potions_to_inventory(potion_sell_list)

        return potion_sell_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[float]) -> list[float]:
        """
        Method to try find the optimal profit for a given starting money value. TO ADD

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
            profit_per_dollar = profit_per_litre/potion_vendor_price
            # Must have a limit to each trade. Instead of basing it on Litres, convert
            # this to maximum money spent per trade
            max_money_spend = litres_available * potion_vendor_price

            # BST can only have unique nodes. So, if two potions have the same profit per dollar, sum them
            # This can be done since they are now essentially the same item
            if profits_tree.__contains__(profit_per_dollar):
                previous_max_money_spend = profits_tree[profit_per_dollar][1]
                profits_tree.__delitem__(profit_per_dollar)
                profits_tree[profit_per_dollar] = [profit_per_dollar, max_money_spend + previous_max_money_spend]
            else:
                profits_tree[profit_per_dollar] = [profit_per_dollar, max_money_spend]

        # Play each day
        for i in range(len(starting_money)):
            player_money = starting_money[i]
            # earnings always starts with the money we start with
            earnings = player_money
            # start from the largest profit trade in the tree, going down
            for k in range(1, len(profits_tree) + 1):
                kth_best_transaction = profits_tree.kth_largest(k).item

                # if the player doesn't have enough for the whole trade,
                # do their maximum and finish the day
                if player_money <= kth_best_transaction[1]:
                    earnings += player_money * kth_best_transaction[0]
                    break

                # They can do the whole trade. Then move on to the next best one
                else:
                    earnings += kth_best_transaction[0]*kth_best_transaction[1]
                    player_money = player_money - kth_best_transaction[1]
            results.append(earnings)

                # if(player_money - profit_list[2]*profit_list[1]) > 0:
                #     earnings += profit_list[3]*profit_list[1]
                #     player_money = player_money - profit_list[2]*profit_list[1]
                #
                # # Cannot buy all stock of most profitable, buys highest possible share of stock
                # else:
                #     quanity = player_money/profit_list[2]
                #     earnings += quanity * profit_list[3]
                #     results.append(earnings)
                #     break

        # for potion in potion_valuations:
        #     #appends into profits where each element is [net profit,litres available,buy price,resell price]
        #     counter = 0
        #
        #
        #     while vendor_available[counter][0] != potion[0]:
        #         if counter > len(potion_valuations): #Vendors not selling potion wanted by adventurers
        #             break
        #         else:
        #             counter += 1
        #
        #     profits.append([potion[1]-self.potion_table[potion[0]].buy_price, vendor_available[counter][1], self.potion_table[potion[0]].buy_price, potion[1]])
        # #profits.sort(reverse=True)
        # #sorts with respect to the 1st element first and then the 3rd element
        # profits.sort(key=lambda a: (a[1],a[3]))
        # #print(profits)

        # for money in starting_money:
        #     earnings = 0
        #     print("Money " + str(money))
        #     for potion in profits:
        #         #Buy price * quantity - available money
        #         if (money - potion[2]*potion[1]) > 0:
        #             earnings += potion[3]*potion[1]
        #             money = money - potion[2]*potion[1]
        #
        #         #Cannot buy all stock of most profitable, buys highest possible share of stock
        #         else:
        #             quantity = money/potion[2]
        #             earnings += quantity * potion[3]
        #             results.append(earnings)
        #             break




        #DANIEL
        # profit_sorted = ArraySortedList(len(potion_valuations))
        #
        # # iterate through each item in potion_valuations:
        # for potion in potion_valuations:
        #     # Price adventurers are willing to pay ($/L)
        #     potion_sell_price = potion[1]
        #
        #     # Price to buy from vendors ($/L)
        #     potion_buy_price = self.potion_table[potion[0]].buy_price
        #
        #     # Profit per litre ($/L)
        #     potion_profit = potion_sell_price - potion_buy_price
        #
        #     profit_sorted.add((potion_profit, potion[0], potion_sell_price))
        #
        # profits = []
        # for i in range(len(starting_money)):
        #     money = starting_money[i]
        #     profits.append(0)
        #     for j in range(len(profit_sorted) - 1, -1, -1):
        #         # Potion currently purchasing
        #         potion_purchasing = self.potion_table[profit_sorted[j][1]]
        #         # Price of current potion
        #         purchase_price = potion_purchasing.buy_price
        #
        #         # Check if enough money to buy out entire stock
        #         purchasable_litres = money / purchase_price
        #
        #         # Purchasable quantity
        #         purchasable_quantity = self.potion_inventory[purchase_price][1]
        #
        #         # if enough money then profit off all of this potion, then go to next
        #         if purchasable_litres >= purchasable_quantity:
        #             profits[i] += purchasable_quantity * profit_sorted[j][2]
        #             money -= purchase_price * purchasable_quantity
        #             print(purchasable_quantity * profit_sorted[j][2])
        #         else:
        #             profits[i] += purchasable_litres * profit_sorted[j][2]
        #             money -= purchase_price * purchasable_litres
        #             print(purchasable_litres * profit_sorted[j][2])
        #             break
        # return profits

        return results
            
            
                

        

                        


        




# G = Game()
# # Setting the potions with the stats: Name, Category, Buying Price from Vendors ($/L)
# G.set_total_potion_data([
# ["Potion of Health Regeneration", "Health", 20],
# ["Potion of Extreme Speed", "Buff", 10],
# ["Potion of Deadly Poison", "Damage", 45],
# ["Potion of Instant Health", "Health", 5],
# ["Potion of Increased Stamina", "Buff", 25],
# ["Potion of Untenable Odour", "Damage", 1]
# ])
#
# G.add_potions_to_inventory([
#     ("Potion of Health Regeneration", 4),
#     ("Potion of Extreme Speed", 5),
#     ("Potion of Instant Health", 3),
#     ("Potion of Increased Stamina", 10),
#     ("Potion of Untenable Odour", 5)
# ])
#
# full_vendor_info = [
#             ("Potion of Health Regeneration", 30),
#             ("Potion of Extreme Speed", 15),
#             ("Potion of Instant Health", 15),
#             ("Potion of Increased Stamina", 20),
#         ]
#
# G.solve_game(full_vendor_info, [12.5, 45, 80])