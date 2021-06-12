#Author: James Carter Garrett

import json
import requests
import sys
import time

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
    #The individual symbol and land count variables
    wSymbol, uSymbol, bSymbol, rSymbol, gSymbol = 0, 0, 0, 0, 0
    plains, islands, swamps, mountains, forests = 0, 0, 0, 0, 0

    #The total card and symbol counts
    cardCount, symbolCount = 0, 0

    if (fileChecker() == False):
        sys.exit()

    with open(sys.argv[1], "r", encoding="utf-8") as ourFile:
        fileContents = ourFile.read()

    splitFile = fileContents.split("\n")

    #Processes the lines
    for lines in splitFile:
        if (lines == "Main" or lines == ''):
            continue

        #Seperates the number of cards from the card name
        splitLines = lines.split(" ", 1)
        print(splitLines)

        #Replaces the spaces with a plus sign so that we can search the full card name through the api
        cardName = splitLines[1].replace(" ", "+")
        searchAddress = "https://api.scryfall.com/cards/named?exact=" + cardName

        try:
            apiRequest = requests.get(searchAddress).json()
            time.sleep(.10)
        except:
            sys.exit("There has been an error")

        #Saves the mana cost and splits it so that it can be counted
        manaCost = apiRequest["mana_cost"].replace("}", "} ")
        splitCost = manaCost.split()

        #Processes the mana cost
        for numberOfCards in range(splitLines[0]):
            cardCount += 1

            for symbols in splitCost:
                currentSymbol = symbols[1]

                if (currentSymbol.isNumeric() or currentSymbol == 'C' or currentSymbol == 's'):
                    #This mana is generic, colorless, or snow, which we will assume the deck can pay for through other cards
                    continue
                
                else:
                    if (currentSymbol == 'W'):
                        wSymbol += 1
                        symbolCount += 1
                    
                    elif (currentSymbol == 'U'):
                        uSymbol += 1
                        symbolCount += 1
                    
                    elif (currentSymbol == 'B'):
                        bSymbol += 1
                        symbolCount += 1
                    
                    elif (currentSymbol == 'R'):
                        rSymbol += 1
                        symbolCount += 1
                    
                    elif (currentSymbol == 'G'):
                        gSymbol += 1
                        symbolCount += 1
                    
                    else:
                        print("A non-valid symbol has been detected. Please make sure all cards in your list are black-bordered cards.")
                        sys.exit()
            
        print(splitCost)
        print()
        print()

        print(searchAddress)


    



decklistReader()