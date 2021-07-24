from selenium import webdriver
import time


def main(fullPath):

    driver = webdriver.Chrome()
    siteName = 'https://www.finecooking.com/recipes-menus?paged=1'
    recipeClassName = 'content-browser__linked-image'
    loadMoreClassName = 'recipe__ajax__pagination__link'
    cacheName = str(fullPath) + '/sites/finecooking/finecooking.txt'
    maxSeen = 50    # how many already seen recipes in a row
                    # till it breaks look and stop scraping the site

    # loading cache
    with open(cacheName, 'r') as cache:
        existing = cache.read().splitlines()

    seenCombo = 0   # how many in a row the bot has seen rn

    while seenCombo < maxSeen:
        driver.get(siteName)
        time.sleep(5)

        recipes = driver.find_elements_by_class_name(recipeClassName)
        print(recipes)
        for recipe in recipes:
            if recipe.get_attribute('href') not in existing:
                print('Adding ' + str(recipe.get_attribute('href'))[36:])
                seenCombo = 0

                with open(cacheName, 'a+') as cache:
                    existing.append(recipe.get_attribute('href') + '\n')
                    cache.write(recipe.get_attribute('href') + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as masterList:
                    masterList.write(recipe.get_attribute('href') + '\n')
            else:
                print('Alread have ' + str(recipe.get_attribute('href'))[36:])
                seenCombo += 1
        
        siteName = siteName[:48] + str(int(siteName[48:]) + 1)
        print('\n\nMoving to page ' + siteName)
        time.sleep(2)

    driver.close()
