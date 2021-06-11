#Author: James Carter Garrett

import json
import requests
import sys

#The individual symbol and land count variables
wSymbol, uSymbol, bSymbol, rSymbol, gSymbol = 0, 0, 0, 0, 0
plains, islands, swamps, mountains, forests = 0, 0, 0, 0, 0

#The total card and symbol counts
cardCount, symbolCount = 0, 0

#Makes sure the file is valid
def fileChecker():
    try:
        ourFile = open(sys.argv[1], "r")
        ourFile.close()
        return True
    except:
        print("This program needs a filename.")
        return False

#The function for reading/processing our file(s)
def decklistReader():
    if (fileChecker() == False):
        sys.exit()

    with open(sys.argv[1], "r") as ourFile:
        fileContents = ourFile.read()
    print(fileContents)

decklistReader()
print("test")