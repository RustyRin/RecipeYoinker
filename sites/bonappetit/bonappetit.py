from selenium import webdriver


def main(fullPath):

    driver = webdriver.Chrome()
    siteName = 'https://www.bonappetit.com/recipes'
    recipeClassName = 'button-2d'
    loadMoreClassName = 'btn-more-channel'
    cacheName = str(fullPath) + '/sites/bonappetit/bonappetit.txt'
    maxSeen = 50    # how many already seen recipes in a row
                    # till it breaks look and stop scraping the site

    # loading cache
    with open(cacheName, 'r') as cache:
        existing = cache.read().splitlines()

    driver.get(siteName)

    seenCombo = 0   # how many in a row the bot has seen rn

    while seenCombo < maxSeen:
        recipes = driver.find_elements_by_class_name(recipeClassName)

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
        
        loadMore = driver.find_element_by_class_name(loadMoreClassName).click()

    driver.close()