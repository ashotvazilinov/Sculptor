import random

mylist = ["apple", "banana", "cherry"]

print(random.choices(mylist, weights = [3], k = 3))