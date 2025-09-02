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

# import json

# # some JSON:
# x =  '{ "name":"John", "age":30, "city":"New York"}'

# # parse x:
# y = json.loads(x)

# # the result is a Python dictionary:
# print(y["age"])

# from simple_salesforce import Salesforce

# sf = Salesforce(
#     username='testing12332311234@gmail.com',
#     password='312312fdsa453',  # Без security token
#     domain='test'  # Указывает, что это sandbox (https://test.salesforce.com)
# )

# # Пример запроса
# accounts = sf.query("SELECT Id, Name FROM Account LIMIT 5")
# print(accounts)

# import pandas as pd

# # читаем файл
# df = pd.read_csv(r"D:\work\Curtis\264\264 - Sheet243 (1).csv", encoding="utf-8")

# new_rows = []

# # обрабатываем по каждому продукту
# for product_id, group in df.groupby("SCLP__Product__c"):
#     # сортируем по текущему порядку, чтобы сохранить исходный
#     group = group.sort_values("SCLP__Order__c").reset_index(drop=True)

#     # выделяем lead и manufacturer
#     lead = group[group["Name"] == "Lead product"]
#     manu = group[group["Name"] == "Manufacturer"]

#     # остальные (кроме этих двух)
#     rest = group[~group["Name"].isin(["Lead product", "Manufacturer"])]

#     # собираем новый порядок
#     new_group = pd.concat([lead, manu, rest], ignore_index=True)

#     # заново проставляем Order
#     new_group["SCLP__Order__c"] = range(1, len(new_group) + 1)

#     new_rows.append(new_group)

# # объединяем всё
# df_new = pd.concat(new_rows)

# # сохраняем
# df_new.to_csv(r"D:\work\Curtis\264\264 - Sheet243 (1).csv", index=False, encoding="utf-8")

# print("Готово! Сохранено в updated_order.csv")

print("Twinkle, twinkle, little star, \n\tHow I wonder what you are! \n\t\tUp above the world so high, \n\t\tLike a diamond in the sky. \nTwinkle, twinkle, little star, \n\tHow I wonder what you are!")

