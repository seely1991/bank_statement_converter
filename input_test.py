import csv

with open("categories.csv", newline='') as file:
    reader = csv.reader(file)
    for cat in reader:
        print(cat[0])
        

x = input("type something\n\n")
print(x)
print (x, " = ", "take me home: ", x == "take me home")  