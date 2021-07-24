from selenium import webdriver
import time

def main(fullPath):

    driver = webdriver.Chrome()
    siteName = 'https://www.publix.com/search/recipes?searchTerm='
    recipeClassName = 'content-wrapper'
    loadMoreClassName = 'loading-button'
    cacheName = str(fullPath) + '/sites/publixaprons/publixaprons.txt'
    maxSeen = 50    # how many already seen recipes in a row
                    # till it breaks look and stop scraping the site

    # loading cache
    with open(cacheName, 'r') as cache:
        existing = cache.read().splitlines()

    driver.get(siteName)
    time.sleep(10)

    try:
        closePopUp = driver.find_element_by_class_name('icon-close')
        closePopUp.click()
    except:
        print()

    seenCombo = 0   # how many in a row the bot has seen rn

    while seenCombo < maxSeen:
        recipes = driver.find_elements_by_class_name(recipeClassName)
        print('poggers')
        for recipe in recipes:
            if recipe.get_attribute('href') not in existing:
                print('Adding ' + str(recipe.get_attribute('href'))[45:])
                seenCombo = 0

                with open(cacheName, 'a+') as cache:
                    existing.append(recipe.get_attribute('href') + '\n')
                    cache.write(recipe.get_attribute('href') + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as masterList:
                    masterList.write(recipe.get_attribute('href') + '\n')
            else:
                print('Alread have ' + str(recipe.get_attribute('href'))[45:])
                seenCombo += 1
        try:
            loadMore = driver.find_element_by_class_name(loadMoreClassName).click()
            time.sleep(5)
        except:
            seenCombo = 999999
        

    driver.close()