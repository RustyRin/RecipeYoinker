'''
This is my first attempt at
category scraping

the idea is that the bot will go
though a list of links to the
categories the site and then go
to each page of that category
then go on to the next category
'''

from selenium import webdriver
import time

categories = [
    "https://www.kingarthurbaking.com/recipes/biscuits-shortcakes",
    "https://www.kingarthurbaking.com/recipes/bread",
    "https://www.kingarthurbaking.com/recipes/buns-rolls",
    "https://www.kingarthurbaking.com/recipes/cake",
    "https://www.kingarthurbaking.com/recipes/chocolates-candies",
    "https://www.kingarthurbaking.com/recipes/coffeecake",
    "https://www.kingarthurbaking.com/recipes/cookies-bars",
    "https://www.kingarthurbaking.com/recipes/crackers",
    "https://www.kingarthurbaking.com/recipes/crisps-cobblers",
    "https://www.kingarthurbaking.com/recipes/doughnuts",
    "https://www.kingarthurbaking.com/recipes/glazes-toppings",
    "https://www.kingarthurbaking.com/recipes/ice-cream-sorbet",
    "https://www.kingarthurbaking.com/recipes/main-dish",
    "https://www.kingarthurbaking.com/recipes/miscellaneous",
    "https://www.kingarthurbaking.com/recipes/muffins-popovers",
    "https://www.kingarthurbaking.com/recipes/pancakes-waffles",
    "https://www.kingarthurbaking.com/recipes/pastry",
    "https://www.kingarthurbaking.com/recipes/pie",
    "https://www.kingarthurbaking.com/recipes/puddings-trifle",
    "https://www.kingarthurbaking.com/recipes/scones"
]

def main(fullPath):

    for category in categories:
        print('\n\n\nWORKING ON CATEGORY ' + str(category))
        driver = webdriver.Chrome()
        
        anotherPage = True
        while anotherPage:
            anotherPage = False
            driver.get(category)
            time.sleep(5)
            for element in driver.find_elements_by_xpath('//a[@aria-label]'):

                if ('Next' in element.get_attribute('aria-label')):
                    pageNext = element
                    print(pageNext)
                    anotherPage = True
                    print('Multiple pages detected...')


            links = driver.find_elements_by_xpath('//a[@href]')

            for link in links:

                if ('-recipe' in str(link.get_attribute('href')) and ('/collections/' not in str(link.get_attribute('href')))):
                    print('FOUND RECIPE ' + link.get_attribute('href'))

            print('anotherPage: ' + str(anotherPage))
            if anotherPage:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print('POGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERSPOGGERS')
                category = pageNext.get_attribute('href')
                #pageNext.click()













        