from selenium import webdriver
import time

def get_all_links(driver, existing):
    time.sleep(2)
    links = []
    elements = driver.find_elements_by_tag_name('a')
    for elem in elements:
        href = elem.get_attribute("href")

        if ('/recipes/' in href) and (href not in existing):
            links.append(href)

    links = list(dict.fromkeys(links))
    return links

def main(fullPath):

    driver = webdriver.Chrome()
    siteName = 'https://altonbrown.com/cook/'
    taget = '_blank'
    loadMoreClassName = 'alm-load-more-btn'
    cacheName = str(fullPath) + '/sites/altonbrown/altonbrown.txt'
    maxSeen = 50    # how many already seen recipes in a row
                    # till it breaks look and stop scraping the site

    # loading cache
    with open(cacheName, 'r') as cache:
        existing = cache.read().splitlines()

    driver.get(siteName)
    time.sleep(10)

    seenCombo = 0   # how many in a row the bot has seen rn

    while seenCombo < maxSeen:
        #recipes = driver.find_elements_by_xpath('//a[@target='+taget)

        recipes = get_all_links(driver, existing)        
        for recipe in recipes:
            if recipe not in existing:
                seenCombo = 0
                print('Adding ' + str(recipe) + ' (SC:' + str(seenCombo) +')')

                with open(cacheName, 'a+') as cache:
                    existing.append(recipe)
                    cache.write(recipe + '\n')

                with open(str(fullPath) + '/recipes.txt', 'a+') as masterList:
                    masterList.write(recipe + '\n')
            else:
                seenCombo += 1
                print('Already have ' + str(recipe) + ' (SC:' + str(seenCombo) +')')
                
        try:
            loadMore = driver.find_element_by_class_name(loadMoreClassName).click()
            time.sleep(2)
        except:
            seenCombo = 999999
        

    driver.close()