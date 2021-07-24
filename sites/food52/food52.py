'''
This file scrapes the vegrecipesofindia.com
site for recipes
'''
import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://food52.com/recipes/newest?page=1'
    className       = 'collectable__img-link'
    cacheName       = str(fullPath) + '/sites/food52/food52.txt'
    recipesOnPage   = True

    while recipesOnPage is True:
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = False
        for i in soup.find_all(class_=className):
            recipeLink = 'https://food52.com' + i['href']
            recipesOnPage = True
            # Read all cached links
            with open(cacheName, 'r') as cache:
                existing = cache.read().splitlines()

            if recipeLink not in existing:
                print("Adding " + recipeLink[28:])

                with open(cacheName, 'a+') as cache:
                    existing.append(recipeLink)
                    cache.write(recipeLink + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                    recipes.write(recipeLink + '\n')
            else:
                print('Alread have ' + recipeLink[28:])
            
        if recipesOnPage is False:
            print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
            recipesOnPage = False
        else:
            print('\n\nMoving to page ' + str(int(siteName[39:]) + 1))
            siteName = siteName[:39] + str(int(siteName[39:]) + 1)
            time.sleep(2)

    


'''
if __name__ == __name__:
    main()
'''