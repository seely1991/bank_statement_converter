import csv
import re
import math

#need to inspect, some items in search key list are identical, but shorter
#e.g. "Amazon" and "AmazonPrime"
#unreliable as to which one will match first

#also, unmatched items will produce duplicates if they have different dates/credit cards etc
#possibly redefine regex to cut off at a certain point that would make duplicates non existent

unmatchedItems = []

def regexLookup(item, listItems, lowerIndex, upperIndex):
    midpoint = math.floor((upperIndex + lowerIndex) / 2)
    searchKey = listItems[midpoint][0]
    itemToCompare = item[4].upper()
    if len(itemToCompare) > len(searchKey[0]):
        itemToCompare = itemToCompare[:len(searchKey)]
    if upperIndex - lowerIndex <= 0 and itemToCompare != searchKey:
        print("match not found for ",itemToCompare)
        print("closest to ", item[4], " is ",searchKey)
        unmatchedItem = {
            "name": item[4],
            "closestMatch": searchKey
        }
        if unmatchedItem not in unmatchedItems:
            unmatchedItems.append(unmatchedItem)
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
        print("reading list...")
        listReader = csv.reader(listFile)
        for listItem in listReader:
            listItems.append(listItem)
    listItems.append([item, category])
    listItems.sort()
    with open("list.csv", "w") as listFile:
        print("writing to list.csv")
        listWriter = csv.writer(listFile)
        for item in listItems:
            listWriter.writerow(item)
            
def askForNewListItem(expenseItem):
    categories = []
    with open("categories.csv",newline='') as catFile:
        for cat in catFile:
            categories.append(cat)
    item = ""
    category = "" 
    characters = 1
    response = "n"
    while characters > 0 and characters < len(expenseItem) and response == "n":
        characters = input("Please type the number of characters to keep from the current list item\n\tType -s to skip this item\n")
        if characters == "-s":
            return None
        if not characters.isdigit() or int(characters) < 1 or int(characters) > len(expenseItem):
            print("This is not a valid number of characters. The value should be a number between 1 and the length of the string to check\n")    
        else:
            characters = int(characters)
            item = expenseItem[:characters]
            print("The entry to be searched will now be: ",item)
            response = input("\tIs this correct? y/n\n")
    while category not in categories:
        category = input("Please type in one of the acceptable categories\n\tTo see a list of acceptable categories, type ls\n\tType -s to skip this item\n")
        if category == "ls":
            for cat in categories:
                print("\t",cat)
            print("\n")
        if category == "-s":
            return None
    print("\nThe following information will be added to the list:\n\t",item,", ",category)
    response = input("Do you wish to continue? y/n\n")
    while response != "n" and response != "y":
        response = input("Please type y/n\n")
    if response == "y":
        addNewListItem(item, category)
        return category
    if response == "n":
        print("Item is not added\nIf you change your mind later, you can edit the list of search keys manually\n")
        return None
        
        
        
    
    

inFile = input("Please specify a filepath\n");
outFile = "output.csv"

if inFile[-4:] != ".csv":
    inFile += ".csv"

listItems = []
prefix = ["PURCHASE AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK AUTHORIZED ON \d\d\/\d\d", "SQ \*", "RECURRING PAYMENT AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK \$\d\d\.\d\d AUTHORIZED ON \d\d\/\d\d ", "PURCHASE WITH CASH BACK \$ \d\d\.\d\d AUTHORIZED ON \d\d\/\d\d ", "PURCHASE RETURN AUTHORIZED ON \d\d\/\d\d "]

with open("list.csv", newline='') as listFile:
    print("reading list.csv...")
    listReader = csv.reader(listFile)
    for listItem in listReader:
        listItem[0] = listItem[0].upper()
        listItems.append(listItem)

listItems.sort()

def convertStatement(inputFilePath, outputFilePath):
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



convertStatement(inFile, outFile)                

                
print("Finished converting statements into ",outputFilePath, "against the following list: ")
print("\n\n\n")


if len(unmatchedItems) > 0:
    response = input("There are some items that were not matched\nWould you like to add them to the list of current know vendors? y/n\n")
    while response != "y" and response != "n":
        response = input("Please type y for yes or n for no\n")
    if response == "y":
        for item in unmatchedItems:
            print("\nMatch not found for ",item["name"])
            print("Closest search key is ",item["closestMatch"])
            askForNewListItem(item["name"])
        convertStatement(inFile, outFile)
            
            
            
for item in listItems:
    print(listItems.index(item),item)