from game import Game

G = Game()
# There are these potions, with these stats, available over the course of the game.
G.set_total_potion_data([
            # Category, Name, Buying price from vendors.
            ["Health", "Potion of Health Regeneration", 20],
            ["Buff", "Potion of Extreme Speed", 10],
            ["Damage", "Potion of Deadly Poison", 45],
            ["Health", "Potion of Instant Health", 5],
            ["Buff", "Potion of Increased Stamina", 25],
            ["Damage", "Potion of Untenable Odour", 1],
        ])

# Start of Day 1
# Let’s begin by adding to the inventory of PotionCorp:
G.add_potions_to_inventory([
    ("Potion of Health Regeneration", 4),
    ("Potion of Extreme Speed", 5),
    ("Potion of Instant Health", 3),
    ("Potion of Increased Stamina", 10),
    ("Potion of Untenable Odour", 5),
])

# Now for choosing vendors!
selling = G.choose_potions_for_vendors(4)
print(selling)
# >>> [
#     ("Potion of Extreme Speed", 5), 
#     ("Potion of Increased Stamina", 10),
#     ("Potion of Health Regeneration", 4),
#     ("Potion of Instant Health", 3),
# ]

# Let’s suppose that the adventurers will pay 30, 15, 15, and 20 dollars per litre for each of the potions listed below.
full_vendor_info = [
    ("Potion of Health Regeneration", 30),
    ("Potion of Extreme Speed", 15),
    ("Potion of Instant Health", 15),
    ("Potion of Increased Stamina", 20),
]

# Play the game with 3 attempts, at different starting money.
results = G.solve_game(full_vendor_info, [12.5, 45, 80])
print(results)
# >>> [37.5, 90, 142.5]
