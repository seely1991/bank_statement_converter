import csv
import re
import math

def regexLookup(item, listItems, lowerIndex, upperIndex):
    midpoint = math.floor((upperIndex + lowerIndex) / 2)
    searchKey = listItems[midpoint][0]
    itemToCompare = item[4].upper()
    if len(itemToCompare) > len(searchKey[0]):
        itemToCompare = itemToCompare[:len(searchKey)]
    if upperIndex - lowerIndex <= 0 and itemToCompare != searchKey:
        print("match not found for ",itemToCompare)
        print("closest to ", item[4], " is ",searchKey)
        newListCategory = askForNewListItem(itemToCompare)
        if newListCategory is not None:
            return newListCategory
        return None
    if itemToCompare == searchKey:
        #print("matched ", item[4]," with ",compare[0])
        return listItems[midpoint][1]
    if itemToCompare < searchKey:
        #print(midpoint, "    ",itemToCompare," < ",searchKey)
        return regexLookup(item, listItems, lowerIndex, midpoint - 1)
    if itemToCompare > searchKey:
        #print(midpoint, "    ",itemToCompare," > ",searchKey)
        return regexLookup(item, listItems, midpoint + 1, upperIndex)
    #print(midpoint, "    ",itemToCompare, " = ", searchKey)
    
def addNewListItem(item, category):
    listItems = []
    with open("list.csv", newline='') as listFile:
        listReader = csv.reader(listFile)
        for listItem in listReader:
            listItems.append(listItem)
    listItems.append([item, category])
    listItems.sort()
    with open("list.csv", newline='') as listFile:
        listWriter = csv.writer(listFile)
        for item in listItems:
            listWriter.writerow(item)
            
def askForNewListItem(expenseItem):
    categories = []
    with open("categories.csv",newline='') as catFile:
        for cat in catFile:
            categories.append(cat[0])
    item = ""
    category = ""
    response = input("List item was not found, would you like to add a search key and category for future queries? y/n\n")
    while response != "n" or response != "y":
        response = input("Please type y/n\n")
    if response == "n":
        return None
    characters = 0
    response = "n"
    while characters > 0 and characters < len(expenseItem) and response == "n":
        characters = input("Please type the number of characters to keep from the current list item")
        item = expenseItem[:characters]
        response = input("The entry to be searched will now be: ",item, " is this correct? y/n\n")
    while category not in categories:
        category = input("Please type in one of the acceptable categories\nTo see a list of acceptable categories, type \"ls\"")
        if category == "ls":
            for cat in categories:
                print(cat)
    response = input("The following information will be added to the list:\n\t",item,", ",category,"\nDo you wish to continue? y/n\n")
    while response != "n" or response != "y":
        response = input("Please type y/n\n")
    if response == "y":
        addNewListItem(item, category)
        return category
    if response == "n":
        print("Item will not be added\nIf you change your mind, you can edit the list of search keys manually")
        return None
        
        
        
    
    

inputFilePath = input("Please specify a filepath\n");
outputFilePath = "output.csv"

if inputFilePath[-4:] != ".csv":
    inputFilePath += ".csv"

listItems = []
prefix = ["PURCHASE AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK AUTHORIZED ON \d\d\/\d\d", "SQ \*", "RECURRING PAYMENT AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK \$\d\d\.\d\d AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK \$ \d\d\.\d\d AUTHORIZED ON \d\d\/\d\d ", "PURCHASE RETURN AUTHORIZED ON \d\d\/\d\d "]

with open("list.csv", newline='') as listFile:
    print("reading list.csv...")
    listReader = csv.reader(listFile)
    for listItem in listReader:
        listItem[0] = listItem[0].upper()
        listItems.append(listItem)

listItems.sort()
        
with open(outputFilePath,"w") as outputFile:
    print("opening output csv...")
    writer = csv.writer(outputFile)
    with open(inputFilePath, newline='') as currentFile:
        print("reading",inputFilePath, "...")
        reader = csv.reader(currentFile)
        for item in reader:
            for fix in prefix:
                replacement = re.sub(fix, "", item[4])
                item[4] = replacement;
            category = regexLookup(item, listItems, 0, len(listItems) - 1)
            item.append(category)
            writer.writerow(item)

print("Finished converting statements into ",outputFilePath, "against the following list: ")
print("\n\n\n")
for item in listItems:
    print(listItems.index(item),item)