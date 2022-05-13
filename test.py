from hash_table import LinearProbePotionTable
from primes import largest_prime
from potion import Potion

hash = LinearProbePotionTable(100, True)
health = Potion("Health Potion", "Milk", 15, 1)
strength = Potion("Strength Potion", "Orange Juice", 20, 2)

print(health.good_hash(health.name,largest_prime(100)))
