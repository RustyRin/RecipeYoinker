'''
This file scrapes the vegrecipesofindia.com
site for recipes
'''
import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.vegrecipesofindia.com/recipes/?fwp_paged=1'
    className       = 'post-summary__image'
    cacheName       = str(fullPath) + '/sites/vegrecipesofindia/vegrecipesofindia.txt'
    recipesOnPage   = True

    while recipesOnPage is True:
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = False
        for i in soup.find_all(class_=className):
            recipeLink = i['href']
            recipesOnPage = True
            # Read all cached links
            with open(cacheName, 'r') as cache:
                existing = cache.read().splitlines()

            if recipeLink not in existing:
                print("Adding " + recipeLink[34:-1])

                with open(cacheName, 'a+') as cache:
                    existing.append(recipeLink)
                    cache.write(recipeLink + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                    recipes.write(recipeLink + '\n')
            else:
                print('Alread have ' + recipeLink[34:-1])
            
        if recipesOnPage is False:
            print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
            recipesOnPage = False
        else:
            print('\n\nMoving to page ' + str(int(siteName[53:]) + 1))
            siteName = siteName[:53] + str(int(siteName[53:]) + 1)
            time.sleep(2)

    


'''
if __name__ == __name__:
    main()
'''