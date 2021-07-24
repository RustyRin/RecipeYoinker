'''
This file scrapes the skinnytaste.com
site for recipes
'''
import requests
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.skinnytaste.com/recipes/page/1'
    className       = 'archive-post'
    cacheName       = str(fullPath) + '/sites/skinnytaste/skinnytaste.txt'
    recipesOnPage   = True

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

            if (recipeLink not in existing) and \
                ('day' not in recipeLink):
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
            print('PAGE NAME ' + siteName[41:])
            print('\n\nMoving to page ' + str(int(siteName[41:]) + 1))
            siteName = siteName[:41] + str(int(siteName[41:]) + 1)
            time.sleep(2)

    