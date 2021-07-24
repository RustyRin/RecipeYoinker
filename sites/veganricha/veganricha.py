'''
This file scrapes the vegrecipesofindia.com
site for recipes
'''
import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.veganricha.com/recipes-with-facets/?fwp_paged=1'
    className       = 'wp-post-image'
    cacheName       = str(fullPath) + '/sites/veganricha/veganricha.txt'
    recipesOnPage   = True
    maxCombo        = 50
    seenCombo       = 0
    while (recipesOnPage is True) and (seenCombo < maxCombo):
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = False

        try:

            for i in soup.find_all(class_=className):
                recipeLink = i['data-pin-url']
                recipesOnPage = True
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if (recipeLink not in existing) and ('recipes' not in recipeLink):
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
                siteName = siteName[:58] + str(int(siteName[58:]) + 1)
                print('\n\nMoving to page ' + siteName)
                time.sleep(2)

        except:
            print('there seems to be no more pages')
            recipesOnPage = False

    


'''
if __name__ == __name__:
    main()
'''