# try:
#     with open('text.txt', 'r', encoding='utf-8') as file:
#         print(file.read())
# except FileNotFoundError:
#     print("lol")

# x = "Hello World!"

# print(len(x))

# mytuple = ("apple", "banana", "cherry")

# print(len(mytuple))

# def myfunc():
#   x = 300
#   def myinnerfunc():
#     print(x)
#   myinnerfunc()

# myfunc()

import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])