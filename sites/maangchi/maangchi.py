'''
This is my first attempt at
category scraping

the idea is that the bot will go
though a list of links to the
categories the site and then go
to each page of that category
then go on to the next category
'''

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib import *
import time


categories = [
    "https://www.maangchi.com/recipes/kimchi",
    "https://www.maangchi.com/recipes/banchan",
    "https://www.maangchi.com/recipes/rice",
    "https://www.maangchi.com/recipes/stews",
    "https://www.maangchi.com/recipes/ricecake",
    "https://www.maangchi.com/recipes/pancakes",
    "https://www.maangchi.com/recipes/noodles",
    "https://www.maangchi.com/recipes/soups",
    "https://www.maangchi.com/recipes/sundubu-jjigae",
    "https://www.maangchi.com/recipes/BBQ",
    "https://www.maangchi.com/recipes/main-dishes",
    "https://www.maangchi.com/recipes/desserts",
    "https://www.maangchi.com/recipes/fried-chicken",
    "https://www.maangchi.com/recipes/one-bowl-meals",
    "https://www.maangchi.com/recipes/easy",
    "https://www.maangchi.com/recipes/fermented",
    "https://www.maangchi.com/recipes/appetizers",
    "https://www.maangchi.com/recipes/dosirak",
    "https://www.maangchi.com/recipes/staple-ingredients",
    "https://www.maangchi.com/recipes/mitbanchan",
    "https://www.maangchi.com/recipes/pickles",
    "https://www.maangchi.com/recipes/beef",
    "https://www.maangchi.com/recipes/non-spicy",
    "https://www.maangchi.com/recipes/spicy",
    "https://www.maangchi.com/recipes/seafood",
    "https://www.maangchi.com/recipes/pork",
    "https://www.maangchi.com/recipes/chicken",
    "https://www.maangchi.com/recipes/porridge",
    "https://www.maangchi.com/recipes/snacks",
    "https://www.maangchi.com/recipes/vegetarian",
    "https://www.maangchi.com/recipes/cold",
    "https://www.maangchi.com/recipes/drinks",
    "https://www.maangchi.com/recipes/not-korean"
]

def main(fullPath):
    #siteName        = 'https://www.vegrecipesofindia.com/recipes/?fwp_paged=1'
    className       = "comp card"
    cacheName       = str(fullPath) + '/sites/maangchi/maangchi.txt'
    recipesOnPage   = True

    for siteName in categories:
        print('\n\n\nWORKING ON CATEGORY ' + siteName)
        recipesOnPage = True
        while recipesOnPage is True:
            req = Request(siteName , headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, "html.parser")
            time.sleep(5)

            # finding all recipes on page
            recipesOnPage = False
            for i in soup.find_all('a', {'href': True}):
                recipeLink = i['href']
                recipesOnPage = True
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if (recipeLink not in existing) and ('/recipe/' in recipeLink):

                    if ('https://www.maangchi.com' not in recipeLink):
                        recipeLink = 'https://www.maangchi.com' + recipeLink


                    print("Adding " + recipeLink)

                    with open(cacheName, 'a+') as cache:
                        existing.append(recipeLink)
                        cache.write(recipeLink + '\n')

                    with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                        recipes.write(recipeLink + '\n')
                else:
                    print('Alread have ' + recipeLink)
                recipesOnPage = False
                
            if recipesOnPage is False:
                print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
                recipesOnPage = False
            
