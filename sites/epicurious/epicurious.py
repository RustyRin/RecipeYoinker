import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.epicurious.com/search?page=1'
    className       = 'view-complete-item'
    cacheName       = str(fullPath) + '/sites/epicurious/epicurious.txt'
    recipesOnPage   = True

    while recipesOnPage is True:
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = False
        for i in soup.find_all(class_=className):
            recipeLink = 'https://www.epicurious.com' + i['href']
            recipesOnPage = True
            # Read all cached links
            with open(cacheName, 'r') as cache:
                existing = cache.read().splitlines()

            if (recipeLink not in existing) and \
                ('expert-advice' not in recipeLink) and \
                ('ingredients' not in recipeLink) and \
                ('shopping' not in recipeLink) and \
                ('video' not in recipeLink) and \
                ('recipes-menus' not in recipeLink) and \
                ('sponsored' not in recipeLink):
                print("Adding " + recipeLink[29:])

                with open(cacheName, 'a+') as cache:
                    existing.append(recipeLink)
                    cache.write(recipeLink + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                    recipes.write(recipeLink + '\n')
            else:
                print('Don\'t need ' + recipeLink[34:-1])
            
        if recipesOnPage is False:
            print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
            recipesOnPage = False
        else:
            print('SITE NAME ' + siteName)
            print('PAGE NAME ' + siteName[39:])
            print('\n\nMoving to page ' + str(int(siteName[39:]) + 1))
            siteName = siteName[:39] + str(int(siteName[39:]) + 1)
            time.sleep(2)

    