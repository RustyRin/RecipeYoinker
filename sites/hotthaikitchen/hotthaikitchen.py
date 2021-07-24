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
    "https://hot-thai-kitchen.com/category/all-recipes/popular-classics/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/street-food/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/quick-meals/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/healthy-meals/page/1",
    "https://hot-thai-kitchen.com/category/pais-kitchen/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/asian-fusion-recipes/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/chickenporkbeef/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/fish-seafood/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/vegetables/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/rice-dishes/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/noodles/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/appetizers/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/entrees/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/rice-and-noodles/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/sweets/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/drinks/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/pastes-sauces/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/holiday-recipes/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/one-dish-meals/page/1",
    "https://hot-thai-kitchen.com/category/stir-fries/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/soups/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/salads/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/curries/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/roasting/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/steaming/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/grilling/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/deep-frying/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/healthy-meals/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/meatless-recipes/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/vegetarian-vegan/page/1",
    "https://hot-thai-kitchen.com/category/all-recipes/sweets/vegan-gluten-free-desserts/page/1"
]

def main(fullPath):
    #siteName        = 'https://www.vegrecipesofindia.com/recipes/?fwp_paged=1'
    className       = "entry-image-link"
    cacheName       = str(fullPath) + '/sites/hotthaikitchen/hotthaikitchen.txt'
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