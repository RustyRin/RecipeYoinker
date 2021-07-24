'''
This file scrapes the vegrecipesofindia.com
site for recipes
'''
import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.budgetbytes.com/category/recipes/page/1'
    className       = 'collectable__img-link'
    cacheName       = str(fullPath) + '/sites/budgetbytes/budgetbytes.txt'
    recipesOnPage   = True
    maxCombo        = 50
    seenCombo       = 0
    while (recipesOnPage is True) and (seenCombo < maxCombo):
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = False

        try:
            soup.findAll(class_="next")
            print('there seems to be more pages')

            for i in soup.find_all('a', {'href': True, 'rel': 'bookmark'}):
                recipeLink = i['href']
                recipesOnPage = True
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if recipeLink not in existing:
                    print("Adding " + recipeLink)
                    seenCombo = 0

                    with open(cacheName, 'a+') as cache:
                        existing.append(recipeLink)
                        cache.write(recipeLink + '\n')

                    with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                        recipes.write(recipeLink + '\n')
                else:
                    print('Alread have ' + recipeLink)
                    seenCombo += 1
                
            if recipesOnPage is False:
                print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
                recipesOnPage = False
            else:
                print('\n\nMoving to page ' + str(int(siteName[-1:]) + 1))
                siteName = siteName[:-1] + str(int(siteName[-1:]) + 1)
                time.sleep(2)

        except:
            print('there seems to be no more pages')
            recipesOnPage = False

    


'''
if __name__ == __name__:
    main()
'''