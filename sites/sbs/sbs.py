'''
This file scrapes the vegrecipesofindia.com
site for recipes
'''

#from re import U
import requests
#import urllib.request
from bs4 import BeautifulSoup
from urllib import *
import time

def main(fullPath):
    siteName        = 'https://www.sbs.com.au/food/recipes/search?search_api_views_fulltext=&page=0'
    className       = 'link-underlay'
    cacheName       = str(fullPath) + '/sites/sbs/sbs.txt'
    recipesOnPage   = True

    while recipesOnPage is True:
        soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')

        # finding all recipes on page
        recipesOnPage = True

        for div_ in soup.find_all(class_='view-empty'):

            print(str(div_.find('p')).lower())

            if 'no results found' in str(div_.find('p')).lower():
                recipesOnPage = False
            
        if recipesOnPage is False:
            print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
            recipesOnPage = False
        else:

            for i in soup.find_all(class_=className):
                recipeLink = i['href']
            
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if (('https://www.sbs.com.au' + recipeLink) not in existing) and \
                    ('blog' not in recipeLink) and \
                    ('article' not in recipeLink) and \
                    ('ondemand' not in recipeLink):

                    print("Adding " + recipeLink[14:])

                    with open(cacheName, 'a+') as cache:
                        existing.append(recipeLink)
                        cache.write('https://www.sbs.com.au' + recipeLink + '\n')

                    with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                        recipes.write('https://www.sbs.com.au' + recipeLink + '\n')
            else:
                print('Don\'t want ' + recipeLink[14:])

            print('\n\nMoving to page ' + str(int(siteName[75:]) + 1))
            siteName = siteName[:75] + str(int(siteName[75:]) + 1)
            time.sleep(2)

    


'''
if __name__ == __name__:
    main()
'''