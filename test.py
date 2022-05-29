# new_list = [('john', 6), ('Micheal', 9), ('George', 2), ('steve', 19)]
#
# new_list.sort(key=lambda y: y[1])
#
# print(new_list)
from hash_table import LinearProbePotionTable

for i in range (3, 100):
    bad_hash_table = LinearProbePotionTable(i, False)
    good_hash_table = LinearProbePotionTable(i, True)
    for j in range(i):
        bad_hash_table.insert(str(j), j)
        good_hash_table.insert(str(j), j)
    # print(str(i) + ": " + str(bad_hash_table.statistics()))
    print(str(i) + ": " + str(good_hash_table.statistics()))