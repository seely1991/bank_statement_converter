import csv
import re
import math

#need to inspect, some items in search key list are identical, but shorter
#e.g. "Amazon" and "AmazonPrime"
#unreliable as to which one will match first
#for now, make sure item will not already be found in search list

#also, unmatched items will produce duplicates if they have different dates/credit cards etc
#possibly redefine regex to cut off at a certain point that would make duplicates non existent
#could use itemToCompare, although this cutoff length is defined by the search key it is looking for and is unreliable

unmatchedItems = []

def regexLookup(item, listItems, lowerIndex, upperIndex):
    midpoint = math.floor((upperIndex + lowerIndex) / 2)
    searchKey = listItems[midpoint][0]
    itemToCompare = item[4].upper()
    if len(itemToCompare) > len(searchKey[0]):
        itemToCompare = itemToCompare[:len(searchKey)]
    if upperIndex - lowerIndex <= 0 and itemToCompare != searchKey:
        #print("match not found for ",itemToCompare)
        #print("closest to ", item[4], " is ",searchKey)
        unmatchedItem = {
            "shortName": itemToCompare,
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
        catReader = csv.reader(catFile)
        for cat in catReader:
            categories.append(cat[0])
    item = ""
    category = "" 
    characters = 1
    print("\n",expenseItem,"was not matched")
    response = input("Would you like to add it to the list of searchable expenses? y/n\n")
    while response != "y" and response != "n":
        response = input("Please type y for yes or n for no\n")
    if response == "n":
        return None
    correct = "n"
    while characters > 0 and characters < len(expenseItem) and correct == "n":
        characters = input("\nPlease type the number of characters to keep from the current list item\n\tType -s to skip this item or -q to quit\n")
        if characters == "-s":
            return None
        if characters == "-q":
            return "-q"
        if not characters.isdigit() or int(characters) < 1 or int(characters) > len(expenseItem):
            print("This is not a valid number of characters. The value should be a number between 1 and the length of the string to check\n")
            characters = 1
        else:
            characters = int(characters)
            item = expenseItem[:characters]
            print("\nThe entry to be searched will now be: ",item)
            correct = input("\tIs this correct? y/n\n")
    while category not in categories:
        category = input("\nPlease type in one of the acceptable categories\n\tTo see a list of acceptable categories, type ls\n\tType -s to skip this item or -q to quit\n")
        if category == "ls":
            for cat in categories:
                print("\t",cat)
            print("\n")
        if category == "-s":
            return None
        if category == "-q":
            return "-q"
    print("\nThe following information will be added to the list:\n\t",item,", ",category)
    response = input("Do you wish to continue? y/n\n")
    while response != "n" and response != "y":
        response = input("Please type y/n\n")
    if response == "y":
        addNewListItem(item, category)
        return category
    if response == "n":
        print("Item was not added\nIf you change your mind later, you can edit the list of search keys manually\n\n")
        return None
        
        
        
    
    

inFile = input("Please specify a filepath\n");
outFile = "output.csv"

if inFile[-4:] != ".csv":
    inFile += ".csv"

listItems = []
prefix = [
             "PURCHASE AUTHORIZED ON ", 
             "PURCHASE WITH CASH BACK AUTHORIZED ON ", 
             "SQ \*", 
             "RECURRING PAYMENT AUTHORIZED ON ", 
             "PURCHASE WITH CASH BACK \$\d\d\.\d\d AUTHORIZED ON ", 
             "PURCHASE WITH CASH BACK \$ \d\d\.\d\d AUTHORIZED ON ", 
             "PURCHASE RETURN AUTHORIZED ON "
         ]

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
                replacement = re.sub("\d\d\/\d\d ","", item[4])
                for fix in prefix:
                    replacement = re.sub(fix, "", replacement)
                    item[4] = replacement;
                category = regexLookup(item, listItems, 0, len(listItems) - 1)
                item.append(category)
                writer.writerow(item)



convertStatement(inFile, outFile)                

                
print("Finished converting statements into ",outFile)


if len(unmatchedItems) > 0:
    print("\n\nThere are", len(unmatchedItems), "items that were not matched") 
    response = input("Would you like to go through and add them to the list of current know vendors? y/n\n")
    while response != "y" and response != "n":
        response = input("Please type y for yes or n for no\n")
    if response == "y":
        for item in unmatchedItems:
            response = askForNewListItem(item["name"])
            if response == "-q":
                break
        convertStatement(inFile, outFile)