'''
This is my first attempt at
category scraping

the idea is that the bot will go
though a list of links to the
categories the site and then go
to each page of that category
then go on to the next category
'''

import requests
from bs4 import BeautifulSoup
from urllib import *
import time


categories = [
    "https://www.manjulaskitchen.com/recipes/appetizers/page/1",
    "https://www.manjulaskitchen.com/recipes/paneer-indian-cheese/page/1",
    "https://www.manjulaskitchen.com/recipes/raita/page/1",
    "https://www.manjulaskitchen.com/recipes/rice/page/1",
    "https://www.manjulaskitchen.com/recipes/sandwiches/page/1",
    "https://www.manjulaskitchen.com/recipes/snacks/page/1",
    "https://www.manjulaskitchen.com/recipes/soups-and-salads/page/1",
    "https://www.manjulaskitchen.com/recipes/vegan/page/1",
    "https://www.manjulaskitchen.com/recipes/curry-gravy/page/1",
    "https://www.manjulaskitchen.com/recipes/sauteed-dry-vegetables/page/1",
    "https://www.manjulaskitchen.com/recipes/instant-pot/page/1",
    "https://www.manjulaskitchen.com/recipes/gluten-free/page/1",
    "https://www.manjulaskitchen.com/recipes/fusion/page/1",
    "https://www.manjulaskitchen.com/recipes/desserts/page/1",
    "https://www.manjulaskitchen.com/recipes/dal-lentils/page/1",
    "https://www.manjulaskitchen.com/recipes/chutneys-pickles/page/1",
    "https://www.manjulaskitchen.com/recipes/chaat/page/1",
    "https://www.manjulaskitchen.com/recipes/breads/page/1",
    "https://www.manjulaskitchen.com/recipes/beverages/page/1"
]

def main(fullPath):
    #siteName        = 'https://www.vegrecipesofindia.com/recipes/?fwp_paged=1'
    className       = 'post-summary__image'
    cacheName       = str(fullPath) + '/sites/manjulaskitchen/manjulaskitchen.txt'
    recipesOnPage   = True

    for siteName in categories:
        print('WORKING ON CATEGORY ' + siteName)
        recipesOnPage = True
        while recipesOnPage is True:
            soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

            # finding all recipes on page
            recipesOnPage = False
            for i in soup.find_all('a', {'href': True, 'rel': 'bookmark'}):
                recipeLink = i['href']
                recipesOnPage = True
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if recipeLink not in existing:
                    print("Adding " + recipeLink)

                    with open(cacheName, 'a+') as cache:
                        existing.append(recipeLink)
                        cache.write(recipeLink + '\n')

                    with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                        recipes.write(recipeLink + '\n')
                else:
                    print('Alread have ' + recipeLink)
                
            if recipesOnPage is False:
                print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
                recipesOnPage = False
            
            else:
                print('\n\nMoving to page ' + str(int(siteName[-1:]) + 1))
                siteName = siteName[:-1] + str(int(siteName[-1:]) + 1)
                time.sleep(2)
            
