# MTGBasicLandCalculator
 This program will process certain MTG decklists and automatically calculate the best ratio for your basic lands.
 
 Currently, this program is meant for EDH / 100 card decks lists, however I plan on adding support for different deck sizes / formats in the future.

# Libraries
 The only external library that currently needs to be installed is the "requests" module.
 
 # How this works
  First off, you will need to create a decklist on "deckstats.net". 
  Then, once you have the deck at the point where you are ready to add basic lands, download the file using deckstat's "tools" button.
  
  ![image](https://user-images.githubusercontent.com/29970309/122498409-11d6f200-cfbd-11eb-92ca-547813ba4672.png)
  
  In the next window, you will want to download your file as a ".txt" file, and make sure to uncheck **"include card comments"**. 
  
  ![image](https://user-images.githubusercontent.com/29970309/122499290-ad1c9700-cfbe-11eb-993b-62263248a7b3.png)

  **This is important, as this program processes decklists with a specific formatting, which the comments can throw off.**
  
  After you have your decklist, you can drag and drop it onto the "**EDHBasicLandCalculator.py**" file. Then, the file will automatically get processed, and the best distribution of lands (according to the formula) will be printed out along with the number of basic lands you'll need and the number of symbols for each color.
