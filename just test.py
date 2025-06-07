try:
    with open('text.txt', 'r', encoding='utf-8') as file:
        print(file.read())
except FileNotFoundError:
    print("lol")