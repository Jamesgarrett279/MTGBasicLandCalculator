# Author: James Carter Garrett

# This is the main file for the mean time. However, as this project progresses, there will be calculators for different formats (Modern, Draft, etc.)


import json
import requests
import sys
import time

# The main function
def main():
    decklistReader()

# Makes sure the file is valid
def fileChecker():
    try:
        ourFile = open(sys.argv[1], "r")
        ourFile.close()
        return True
    except:
        print("This program needs a filename.")
        return False

# This is our formula
def landFormula(bLands, symbolCount, totalSymbols):
    return (symbolCount / totalSymbols) * bLands

# This function processes special cards with multiple faces
def specialProcessor(apiRequest, cardName):
    # The counts for each side
    s1Count, s1W, s1U, s1B, s1R, s1G = 0, 0, 0, 0, 0, 0
    s2Count, s2W, s2U, s2B, s2R, s2G = 0, 0, 0, 0, 0, 0
    countSum, wSum, uSum, bSum, rSum, gSum = 0, 0, 0, 0, 0, 0
    s1Land, s2Land = True, True

    # Gets the mana costs for each side
    side1 = apiRequest['card_faces'][0]["mana_cost"].replace("}", "} ")
    side2 = apiRequest['card_faces'][1]["mana_cost"].replace("}", "} ")

    # Checks to see if either side are lands / no mana cost
    if (side1 != ""):
        s1Split = side1.split()
        s1Land = False
    
    if (side2 != ""):
        s2Split = side2.split()
        s2Land = False

    # Processes the sides if they aren't lands / no mana cost
    if (s1Land == False):
        s1Results = processCards(s1Split, cardName)

        s1Count = s1Results[0]
        s1W = s1Results[1]
        s1U = s1Results[2]
        s1B = s1Results[3]
        s1R = s1Results[4]
        s1G = s1Results[5]

    if (s2Land == False):
        s2Results = processCards(s2Split, cardName)

        s2Count = s2Results[0]
        s2W = s2Results[1]
        s2U = s2Results[2]
        s2B = s2Results[3]
        s2R = s2Results[4]
        s2G = s2Results[5]
    
    # Calculates and returns the sum of each counts
    countSum = (s1Count + s2Count)
    wSum = (s1W + s2W)
    uSum = (s1U + s2U)
    bSum = (s1B + s2B)
    rSum = (s1R + s2R)
    gSum = (s1G + s2G)

    return (countSum, wSum, uSum, bSum, rSum, gSum)

# This is our function for processing the cards and their symbols
def processCards(splitCost, cardName):
    symbolCount, wSymbol, uSymbol, bSymbol, rSymbol, gSymbol = 0, 0, 0, 0, 0, 0
    numbers = "0123456789"

    # Processes the mana symbols
    for symbols in splitCost:
        currentSymbol = symbols[1]

        if (currentSymbol in numbers or currentSymbol == 'C' or currentSymbol == 'S' or currentSymbol == 'X'):
            # This mana is generic, colorless, or snow, which we will assume the deck can pay for through other cards
            continue
        
        # Checks for each mana type
        else:
            # Normal Symbols
            if (symbols == "{W}"):
                wSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{U}"):
                uSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{B}"):
                bSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{R}"):
                rSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{G}"):
                gSymbol += 1
                symbolCount += 1
            
            # Phyrexian Symbols
            elif (symbols == "{W/P}"):
                wSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{U/P}"):
                uSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{B/P}"):
                bSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{R/P}"):
                rSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{G/P"):
                gSymbol += 1
                symbolCount += 1

            # 2 Generic Mana or One Normal
            elif (symbols == "{2/W}"):
                wSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{2/U}"):
                uSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{2/B}"):
                bSymbol += 1
                symbolCount += 1

            elif (symbols == "{2/R}"):
                rSymbol += 1
                symbolCount += 1
            
            elif (symbols == "{2/G}"):
                gSymbol += 1
                symbolCount += 1
            
            # Dual Symbols
            elif (symbols == "{W/U}"):
                wSymbol += 0.5
                uSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{W/B}"):
                wSymbol += 0.5
                bSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{B/R}"):
                bSymbol += 0.5
                rSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{B/G}"):
                bSymbol += 0.5
                gSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{U/B}"):
                uSymbol += 0.5
                bSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{U/R}"):
                uSymbol += 0.5
                rSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{R/G}"):
                rSymbol += 0.5
                gSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{R/W}"):
                rSymbol += 0.5
                wSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{G/W}"):
                gSymbol += 0.5
                wSymbol += 0.5
                symbolCount += 1
            
            elif (symbols == "{G/U}"):
                gSymbol += 0.5
                uSymbol += 0.5
                symbolCount += 1
            
            # If the symbol is not one of the above cases, it's either not a symbol or it's from an un-set
            else:
                print("A non-valid symbol has been detected. Please make sure all cards in your list are black-bordered cards.")
                print("Card Name: " + cardName)
                sys.exit("Error with a card.")
    
    # Returns the correct values as a tuple
    return (symbolCount, wSymbol, uSymbol, bSymbol, rSymbol, gSymbol)   

# The function for reading/processing our file(s)
def decklistReader():
    # The individual symbol and land count variables
    wSymbol, uSymbol, bSymbol, rSymbol, gSymbol = 0, 0, 0, 0, 0
    plains, islands, swamps, mountains, forests = 0, 0, 0, 0, 0

    # The total card and symbol counts
    cardCount, symbolCount = 0, 0

    if (fileChecker() == False):
        return

    with open(sys.argv[1], "r", encoding="utf-8") as ourFile:
        fileContents = ourFile.read()

    splitFile = fileContents.split("\n")

    # Processes the lines of the file
    for lines in splitFile:
        # Our boolean for special cards
        specialCard = False

        if (lines == "Main" or lines == ''):
            continue

        # Seperates the number of cards from the card name
        splitLines = lines.split(" ", 1)

        # Replaces the spaces with a plus sign so that we can search the full card name through the api
        cardName = splitLines[1].replace(" ", "+")
        searchAddress = "https://api.scryfall.com/cards/named?exact=" + cardName

        try:
            api = requests.get(searchAddress)

            if (api.status_code != 200):
                print(api.status_code)
            
            if (api.status_code == 404):
                print("Error: Card not found")
                return

            apiRequest = api.json()
            time.sleep(.05)

        except Exception as ex:
            print(ex)
            return

        # Checks to see if the card is a special type by looking for the "card_faces" key
        if ("card_faces" in apiRequest):
                specialCard = True
        
        # If the card isn't special, split the mana cost
        else:
            # Check to see if the card is a land / has no mana cost, going to the next card if it is
            if (apiRequest["mana_cost"] == ""):
                cardCount += int(splitLines[0])
                continue

            else:
                # Saves the mana cost and splits it so that it can be counted
                manaCost = apiRequest["mana_cost"].replace("}", "} ")
                splitCost = manaCost.split()

        # Processes the cards
        for numberOfCards in range(int(splitLines[0])):
            cardCount += 1

            if (specialCard == True):
                returnedMana = specialProcessor(apiRequest, cardName)
            
            else:
                returnedMana = processCards(splitCost, cardName)
            
            # Increases the mana values
            symbolCount += returnedMana[0]
            wSymbol += returnedMana[1]
            uSymbol += returnedMana[2]
            bSymbol += returnedMana[3]
            rSymbol += returnedMana[4]
            gSymbol += returnedMana[5]

    # Calculations
    basicLands = (100 - cardCount) # 100 can be changed depending on the format

    if (cardCount != 0 and cardCount > 0):
        plains = str(landFormula(basicLands, wSymbol, symbolCount))
        islands = str(landFormula(basicLands, uSymbol, symbolCount))
        swamps = str(landFormula(basicLands, bSymbol, symbolCount))
        mountains = str(landFormula(basicLands, rSymbol, symbolCount))
        forests = str(landFormula(basicLands, gSymbol, symbolCount))

    else:
        print("There are either no cards with mana costs in the list or your decklist is full, so the conversion will not run.")
        return

    # Print out the information (this will eventually be in a gui)
    print("Your total basic lands count is: " + str(basicLands))
    print()
    print("The number of plains you should have is: " + plains + " || Symbol Count: " + str(wSymbol))
    print("The number of islands you should have is: " + islands + " || Symbol Count: " + str(uSymbol))
    print("The number of swamps you should have is: " + swamps + " || Symbol Count: " + str(bSymbol))
    print("The number of mountains you should have is: " + mountains + " || Symbol Count: " + str(rSymbol))
    print("The number of forests you should have is: " + forests + " || Symbol Count: " + str(gSymbol))

if __name__ == "__main__":
    print("Running program...")
    print()

    main()

    print()
    input("Press enter to end the program.")