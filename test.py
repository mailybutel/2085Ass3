from hash_table import LinearProbePotionTable
from primes import largest_prime

hash = LinearProbePotionTable(100,True,50)

hash["daniel"] = 135690
hash["maily"] = 12413
hash["josh"] = 39875

print(hash)
