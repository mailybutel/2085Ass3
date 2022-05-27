from game import Game
from hash_table import LinearProbePotionTable
from primes import largest_prime
from potion import Potion

# bad_hash_table = LinearProbePotionTable(70, False)
# good_hash_table = LinearProbePotionTable(70, True)
# health = Potion("Health Potion", "Milk", 15, 1)
# strength = Potion("Strength Potion", "Orange Juice", 20, 2)

# print(health.good_hash(health.name,largest_prime(100)))

for i in range (3, 100):
    bad_hash_table = LinearProbePotionTable(i, False)
    good_hash_table = LinearProbePotionTable(i, True)
    for j in range(i):
        bad_hash_table.insert(str(j), j)
        good_hash_table.insert(str(j), j)
    # print(str(i) + ": " + str(bad_hash_table.statistics()))
    print(str(i) + ": " + str(good_hash_table.statistics()))


# for i in range(1, 70):
#     bad_hash_table.insert(str(i), i)
#     print(bad_hash_table.statistics())
#     good_hash_table.insert(str(i), i)
#     print(good_hash_table.statistics())

# print(bad_hash_table)
# print(good_hash_table)

# make excel sheet based on results
# explain results with graph in pdf

# g = Game()
# g.set_total_potion_data([
#     (str(x), str(x), x)
#     for x in range(1, 101)
# ])
# g.add_potions_to_inventory([
#     (str(x), x)
#     for x in range(2, 101)
# ])
# g.potion_inventory.draw()