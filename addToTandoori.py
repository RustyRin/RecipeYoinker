'''
This script is to scan the top
recipe link in recipes.txt
get all the information it can
and then format that information
in a way that I like to paste
into Tandoori Recipes as a new
recipe.
'''

from http.client import responses
from re import M
import re
import urllib
import urllib.request   
from selenium import webdriver
import time
import os
from selenium.webdriver.common import action_chains
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from titlecase import titlecase
from fractions import Fraction
import ingredientFilter
import sys 
import unicodedata
from PIL import Image

units = [
    'fluid ounces',
    'sticks',
    "quarts",
    "big pinches",
    "pinch",
    "big pinch",
    "small pinch",
    "pound",
    "pounds",
    "tablespoons",
    "tablespoon",
    "leaves",
    "sheet",
    "sheets",
    "container",
    "splash",
    "racks",
    "sprinkle",
    "quart",
    "mug",
    "mugs",
    "heaping teaspoons",
    "gallon",
    "gallons",
    "clove",
    "tiny splash",
    "cups",
    "cup",
    "envelope",
    "small pinch",
    "stick",
    "disk",
    "ml",
    "links",
    "pint",
    "large bunch",
    "box",
    "small handfull",
    "ounces",
    "ounce",
    "small bunch",
    "head",
    "heads",
    "strips",
    "strip",
    "drops",
    "drop",
    "slices",
    "slice",
    "dash",
    "dashes",
    "springs",
    "spring",
    "ears",
    "ear",
    "can",
    "cans",
    "pinch",
    "pinches",
    "packet",
    "packets",
    "packages",
    "package",
    "handful",
    "handfulls",
    "stalk",
    "stalks",
    "bunch",
    "bunches",
    "pound",
    "pounds",
    "cloves",
    "clove",
    "inch",
    "inches",
    "to taste",
    "teaspoon",
    "teaspoons",
    "cup",
    "cups",
    "count",
    "tablespoon",
    "tablespoons",
    "g",
    "grams",
    "milliliters",
    "ounce",
    "ounces",
    "lbs",
    'lb',
    'tbsp',
    'tsp',
    'kg',
    'tbs',
    'grams',
    'oz',
    'packet',
    'lb.',
    'lbs.',
    'lb',
    'lbs',
    'tbs.'
]

fracChars = [
    '¼', 
    '½', 
    '¾', 
    '⅐', 
    '⅑', 
    "⅒", 
    '⅓', 
    '⅔', 
    '⅕', 
    '⅖', 
    '⅗',
    '⅘', 
    '⅙', 
    '⅚', 
    '⅛', 
    '⅜', 
    '⅝', 
    '⅞'
]

def containsNumber(value):
    return any([char.isdigit() for char in value])

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def fracCharToFloat(line):


    dict = {
        '¼': .25,
        '½': .5,
        '¾': .75,
        '⅐': (1/7),
        '⅑': (1/9),
        "⅒": .1,
        '⅓': .333,
        '⅔': .666,
        '⅕': .2,
        '⅖': .4,
        '⅗': .6,
        '⅘': .8,
        '⅙': .166,
        '⅚': .833,
        '⅛': .125,
        '⅜': .375,
        '⅝': .625,
        '⅞': .875
    }

    total = 0.0
    try:
        if len(line) == 1:
            v = unicodedata.numeric(line)
        elif line[-1].isdigit():
            # normal number, ending in [0-9]
            v = float(line)
        else:
            # Assume the last character is a vulgar fraction
            v = float(line[:-1]) + unicodedata.numeric(line[-1])
    except:
        print('EXCEPTION IN TURNING LINE TO FLOAT IN fracCharToFloat')
        raise Exception
        v = 0
    '''
    for char in line:

        try:
            total += (float(char))
        except:
            total += float(dict[char])
            '''
    '''
    for x in dict:
        line = line.replace(x, dict[x])
        line = line.replace(' ' + dict[x], ' 0' + dict[x])
    '''
    return v

class recipe:
    def __init__(
                    self,
                    url = "",
                    title = "",
                    description = "",
                    ingredients = [],
                    prep = [],
                    steps = [],
                    tips = [],
                    timeActive = "",
                    timeWaiting = "",
                    servingUnit = "",
                    servingAmount = "",
                    author = "",
                    calories = "",
                    carbs = "",
                    fats = "",
                    proteins = "",
                    tags = []):
        self.url = url
        self.title = title 
        self.description = description 
        self.ingredients = ingredients
        self.prep = prep
        self.steps = steps
        self.tips = tips 
        self.timeActive = timeActive 
        self.timeWaiting = timeWaiting
        self.servingUnit = servingUnit
        self.servingAmount = servingAmount
        self.author = author
        self.calories = calories
        self.carbs = carbs 
        self.fats = fats 
        self.proteins = proteins
        self.tags = tags

def textTime(string):
    string = string.split()

    timeInMin = 0
    index = 0

    # assuming # -> days -> # -> hours -> # -> min

    while True:
        try:
            if ('day' or 'days' or 'd') in string[index + 1].lower():
                timeInMin += int(string[index])*1440
            elif ('hrs' or 'hr' or 'hours' or 'hour') in string[index + 1].lower():
                timeInMin += int(string[index])*60
            elif ('min' or "mins" or 'minute' or 'minutes') in string[index + 1].lower():
                timeInMin += int(string[index])
            else:
                print('ERROR IN GETTING TIME IN ' + str(string))
                break
        except IndexError:
            break

        index += 2
    
    return timeInMin

def convertToFloat(frac_str):
    '''
    iirc this converts
    fractions in the #/#
    style to floats
    '''
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

def textToIngredient(string, prep=""):

    '''
    Some notes

    this does not yet support
    adding to prep work

    maybe take in prep and then send it off to
    ingredient filter and append any notes that it has

    This does noy yet support
    "1 to 2 ounces"
    i don't know how i would
    support such variable amounts

    maybe just take the first one and then add into notes, idk
    '''

    ingredientItem = [0.000, "", ""]

    # removes everything in parenteses and brackets
    nb_rep = 1
    while (nb_rep):
        (string, nb_rep) = re.subn(r'\([^()]*\)', '', string)

    ingredient = string

    # some places like to do tsp. instead of just tsp
    # this is to make things more uniform
    # i might have to move this in the future
    # if a site uses floats for ingredient amount
    ingredient = ingredient.replace('tsp.', 'tsp')


    ingredient = re.sub('[\(\[].*?[\)\]]', "", ingredient)
    ingredient = re.sub(' +', ' ', ingredient)
    #print('ingredient = ' + str(float(ingredient)) + '\n')

    print('if there is any variable words, replace them')
    try:
        ingredient = re.sub(' to ', '-', ingredient)
    except:
        pass

    # split string by spaces
        # this should get whatever the first element is
        # assuming that the first element will be the amount
        # and the second one is the unit
    ingredientList = ingredient.split()

    # bon appetit likes to split their fractions for
    # some reason, try to see if the fractions is split
    try:
        print('seconds thins in ingredient list = ' + ingredientList[1])
        if ingredientList[1].startswith('/'):
        #if '/' in ingredientList[1]:
            print('detected split fraction in ' + str(ingredientList))
            newList = ['']
            newList[0] = str(ingredientList[0] + ingredientList[1])
            ingredientList.pop(0)
            ingredientList.pop(0)
            newList.extend(ingredientList)
            ingredientList = newList
            print('tried to remove fraction to' + str(ingredientList))
    except:
        pass
        

    # if string starts with a number or fraction
        # then its a good chance a # unit ingredient entry
        # need to filter out # ingredient types (no units, so its count)
        # so maybe have a known list of things to flag
        # so like if it tries to read the unit and it
        # sees for example "large" it should know
        # that the unit is "count" and the ingredient
        # name is whatever that is large

    print('ingredientList = ' + str(ingredientList))
    try:                # trying to make the amount into float

        print('trying to convert the first element to float')

        # is the first element a combination of amount and unit (i.e 70g)
        if 'g' in ingredientList[0]:
            print('ingredient has g in amount')
            amountAndUnitSplit = re.findall(r'[A-Za-z]+|\d+', ingredientList[0])
            print('amountAndUnitSplit = ' + str(amountAndUnitSplit))
            ingredientList[0] = amountAndUnitSplit[0]
            ingredientList.insert(1, amountAndUnitSplit[1])

        ingredientItem[0] += float(ingredientList[0])
        ingredientList = ingredientList[1:]

        # is the next element a fraction character?

        fracChars = ['¼', '½', '¾', '⅐', '⅑', "⅒", '⅓', '⅔', '⅕', '⅖', '⅗', '⅘', '⅙', '⅚', '⅛', '⅜', '⅝', '⅞']
        if ingredientList[0] in fracChars:
            print('the next is a fraction character; raising exception')
            raise ValueError
        else:
            print('the next char does not seem to be a frac char')
            print('trying to see if the next element is a #/# fraction')

            if containsNumber(ingredientList[0]):
                print('pog')

                ingredientList[0] = convertToFloat(ingredientList[0])
                print('ingredientList[0] = ' + str(ingredientList[0]))
                ingredientItem[0] += float(ingredientList[0])
                ingredientList = ingredientList[1:]
            else:
                print('pog?')

        if '-' in ingredientList[0]:
            print('#-# variable ingredient seen')
            numbers = ingredientList[0].split('-')
            try:
                numbers[0] = float(numbers[0])
                numbers[1] = float(numbers[1])
            except:
                try:
                    numbers[0] = convertToFloat(numbers[0])
                    numbers[1] = convertToFloat(numbers[1])
                except:
                    numbers[0] = fracCharToFloat(numbers[0])
                    numbers[1] = fracCharToFloat(numbers[1])
            ingredientList[0] = float((float(numbers[1]) + float(numbers[0])) / 2)

        print(ingredientList)
        ingredient = ingredientList                      # remove the number

        # seeing if the next element is in the known unit array

        print('removed the first element (which is expected to be the amount)')
        print('amount = ' + str(ingredientItem[0]))
        print('ingredient = ' + str(ingredient))

        # here it should scan each word for
        # a unit, there are a bunch of units
        # in the unit array/list above

        if str(ingredientList[0]).lower() in units:
            # the first element is a known unit

            # if it is metric, don't titlecase
            # or an ugly unit a site uses
            if (str(ingredientList[0]).lower()) == 'g':
                ingredientItem[1] = 'Grams'
            elif (str(ingredientList[0]).lower()) == 'ml':
                ingredientItem[1] = 'Milliliters'
            elif (str(ingredientList[0]).lower()) == 'kg':
                ingredientItem[1] = 'Kilograms'
            elif (str(ingredientList[0]).lower()) == 'tbs':
                ingredientItem[1] = 'Tablespoon'
            elif (str(ingredientList[0]).lower()) == 'tbs.':
                ingredientItem[1] = 'Tablespoon'
            elif (str(ingredientList[0]).lower()) == 'tbsp':
                ingredientItem[1] = 'Tablespoon'
            elif (str(ingredientList[0]).lower()) == 'tbsp.':
                ingredientItem[1] = 'Tablespoon'
            elif (str(ingredientList[0]).lower()) == 'tsp':
                ingredientItem[1] = 'Teaspoon'
            elif (str(ingredientList[0]).lower()) == 'lb':
                ingredientItem[1] = 'Pounds'
            elif (str(ingredientList[0]).lower()) == 'lbs':
                ingredientItem[1] = 'Pounds'
            elif (str(ingredientList[0]).lower()) == 'lb.':
                ingredientItem[1] = 'Pounds'
            elif (str(ingredientList[0]).lower()) == 'oz':
                ingredientItem[1] = 'Ounces'
            else:
                # add it to the ingredient list
                ingredientItem[1] = titlecase(ingredientList[0])

            # we saved it so we can remove it
            ingredientList = ingredientList[1:]

            ingredientItem[2] = titlecase(' '.join(ingredientList))

        # if it cannot find a unit, have the
        # default be no unit (meaning, the unit
        # be initialize with "No_Unit")
        else:
             ingredientItem[1] = "Count"
             ingredientItem[2] = titlecase(' '.join(ingredientList))

    except ValueError:  # it might be a fraction

        print('got valueError while trying to convert the first element to float')
        print('expecting this to be a string fraction')
        try:    # now testing if this is a string fraction or just a one cout of something

            # im lazy, this is to save
            # the amount gets modified 
            # so just save it while it gets
            # modified
            old_amount = ingredientList[0]
            print('Trying to find variable amount')
            if '-' in ingredientList[0]:
                print('#-# variable ingredient seen')
                numbers = ingredientList[0].split('-')
                try:
                    numbers[0] = float(numbers[0])
                    numbers[1] = float(numbers[1])
                    print('numbers: ' + str(numbers))
                except:
                    try:
                        print('got error with straight float for variable, using convert to float')
                        numbers[0] = convertToFloat(numbers[0])
                        numbers[1] = convertToFloat(numbers[1])
                        ingredientItem[0] = float((float(numbers[1]) + float(numbers[0])) / 2)
                        print('numbers: ' + str(numbers))
                    except:
                        print('got error converting varable amount with convert to float, using frac char to float')
                        numbers[0] = fracCharToFloat(numbers[0])
                        numbers[1] = fracCharToFloat(numbers[1])
                        ingredientItem[0] = float((float(numbers[1]) + float(numbers[0])) / 2)
                        print('numbers: ' + str(numbers))
                ingredientItem[0] = float((float(numbers[1]) + float(numbers[0])) / 2)
            else:
                print('Did not find variable amount')
                # trying if the first element is a fraction char
                try:
                    print('trying to see if the amount is using frac char')
                    ingredientItem[0] += fracCharToFloat(ingredientList[0])
                except:
                    print('the amount isnt using fraction chars, trying normal fractions')
                    ingredientItem[0] += convertToFloat(ingredientList[0])

            ingredient = ingredientList.pop(0)                      # remove the number

            # here it should scan each word for
            # a unit, there are a bunch of units
            # in the unit array/list above

            if str(ingredientList[0]).lower() in units:
                # the first element is a known unit

                if (str(ingredientList[0]).lower()) == 'g':
                    ingredientItem[1] = 'Grams'
                elif (str(ingredientList[0]).lower()) == 'ml':
                    ingredientItem[1] = 'Milliliters'
                elif (str(ingredientList[0]).lower()) == 'kg':
                    ingredientItem[1] = 'Kilograms'
                elif (str(ingredientList[0]).lower()) == 'tbs':
                    ingredientItem[1] = 'Tablespoon'
                elif (str(ingredientList[0]).lower()) == 'tbsp':
                    ingredientItem[1] = 'Tablespoon'
                elif (str(ingredientList[0]).lower()) == 'tsp':
                    ingredientItem[1] = 'Teaspoon'
                elif (str(ingredientList[0]).lower()) == 'lb':
                    ingredientItem[1] = 'Pounds'
                elif (str(ingredientList[0]).lower()) == 'oz':
                    ingredientItem[1] = 'Ounces'
                else:
                    # add it to the ingredient list
                    ingredientItem[1] = titlecase(ingredientList[0])

                # add it to the ingredient list
                #ingredientItem[1] = titlecase(ingredientList[0])

                # we saved it so we can remove it
                ingredientList = ingredientList[1:]

                ingredientItem[2] = titlecase(' '.join(ingredientList))

            # if it cannot find a unit, have the
            # default be no unit (meaning, the unit
            # be initialize with "No_Unit")
            else:
                ingredientItem[1] = "Count"
                ingredientItem[2] = titlecase(' '.join(ingredientList))
        except:     # this element does not start with a number, so its a one count
            ingredientItem[0] = 0.000
            ingredientItem[1] = "Count"
            ingredientItem[2] = titlecase(' '.join(ingredientList))

    except:               # we've tried everything, must be amount = 0

        print('something happened that I didn\' expect, trying some wild stuff')

        # there is no number
        # so this is just the name of the ingredient
        print('ingredient = ' + str(ingredient))
        ingredientItem[0] = 0.000
        ingredientItem[1] = "No_Unit"
        ingredientItem[2] = titlecase(ingredient)

    print('ingredient item = ' + str(ingredientItem))
    print(
        '-------------------------------------------------------------------------------'
    )


    ingredientItem[1] = titlecase(ingredientItem[1])
    return ingredientItem

    #if (isinstance(ingredientList[0], int) or isinstance(ingredientList[0], float))


    # if it doesnt start with a nunmber
        # it assumes there is no unit and no amount
        # so unit is "No_Unit" with an amount of 0

def addToTandoori(driverTandoori, recipeObject):

    driverTandoori.get('http://192.168.1.15/new/recipe/')
    time.sleep(2)

    try:
        # Do I have to log in?

        # username
        textBox = driverTandoori.find_element_by_id('id_login')
        textBox.send_keys('J')

        # password
        textBox = driverTandoori.find_element_by_id('id_password')
        textBox.send_keys('porven1016')

        # remember me
        button = driverTandoori.find_element_by_id('id_remember')
        button.click()

        # sign in
        button = driverTandoori.find_element_by_xpath("//button[contains(text(), 'Sign In')]")
        button.click()
    except:
        pass

    # input recipeName
    textBox = driverTandoori.find_element_by_id('id_name')
    textBox.send_keys(recipeObject["title"])

    # save button
    button = driverTandoori.find_element_by_xpath("//button[contains(text(), 'Save')]")
    button.click()

    '''
    This is where things get wild

    '''

    driverTandoori.get(driverTandoori.current_url)
    driverTandoori.implicitly_wait(1)

    if recipeObject["image"] != None:
        image = driverTandoori.find_element_by_xpath('//input[@type="file"]')
        image.send_keys(os.getcwd() + '\\recipe.png')
    else:
        print('no image')

    #print(str(ingredientFilter.main(recipeObject["ingredients"], recipeObject["prep"])))

    # input description
    if recipeObject["description"] is not (None or ''):
        textBox = driverTandoori.find_element_by_xpath('//textarea[@id="id_description"]')
        textBox.send_keys(recipeObject["description"])
    
    if recipeObject["timeActive"] is not (None or 0):
        textBox = driverTandoori.find_element_by_xpath('//input[@id="id_prep_time"]')
        textBox.send_keys(recipeObject["timeActive"])

    if recipeObject["timeWaiting"] is not (None or 0):
        textBox = driverTandoori.find_element_by_xpath('//input[@id="id_wait_time"]')
        textBox.send_keys(recipeObject["timeWaiting"])

    if recipeObject["servingsAmount"] is not (None or 0):
        textBox = driverTandoori.find_element_by_xpath('//input[@id="id_servings"]')
        textBox.clear()
        textBox.send_keys(recipeObject["servingsAmount"])

    if recipeObject["servingsUnit"] is not (None or ""):
        textBox = driverTandoori.find_element_by_xpath('//input[@id="id_servings_text"]')
        textBox.clear()
        textBox.send_keys(recipeObject["servingsUnit"])

    if recipeObject["steps"] is not (None or []):
        textBox = driverTandoori.find_element_by_xpath('//div[@class="col-md-12"]')
        textBox = driverTandoori.find_element_by_xpath(".//textarea[@spellcheck='false']")


        #textBox = driverTandoori.find_element_by_xpath('//textarea[@id="id_instruction_523"]')
        
        if recipeObject["author"] is not (None or "") and (recipeObject["url"] is not (None or "")):
            textBox.send_keys('[Made by ' + str(recipeObject["author"]) + '](' + str(recipeObject["url"]) + ')\n\n---\n\n')

        if recipeObject["prep"]:
            print('RECIPE PREP IS NOT EMPTY')
            print(recipeObject["prep"])

            textBox.send_keys('###Prep\n')

            for prepStep in recipeObject["prep"]:
                textBox.send_keys(prepStep + '\n')

            textBox.send_keys('\n\n---\n\n')


        # actually doing the steps now
        textBox.send_keys('##Steps\n')
        for step in recipeObject["steps"]:
            textBox.send_keys(str(recipeObject["steps"].index(step)+1) + '. ' + step + '\n\n')

    if recipeObject["ingredients"] is not (None or []):
        
        addIngredientButton = driverTandoori.find_element_by_class_name('col-md-2')
        addIngredientButton = addIngredientButton.find_element_by_tag_name('button')
        #addIngredientButton.click()
        row = 0
        

        # [AMOUNT OF INGRED, UNIT OF INGRED, INGRED NAME]
        for ingredient in recipeObject["ingredients"]:

            driverTandoori.execute_script("arguments[0].scrollIntoView()", addIngredientButton)
            addIngredientButton.click()

            
            print('WORKING WITH ROW ' + str(row))

            # amount
            textBox = driverTandoori.find_elements_by_xpath('//input[@type="number"]')[row]
            textBox.clear()
            
            try:
                textBox.send_keys(round(ingredient[0], 3))
            except:
                textBox.send_keys(format(ingredient[0], '.3f'))
            

            # unit
            # vvv this does find it
            #textBox = driverTandoori.find_element_by_id("unit_0_" + str(row))
            #textBox.send_keys(ingredient[1])
            '''
            actionChains = ActionChains(driverTandoori)
            actionChains.move_to_element(textBox).click().perform()
            actionChains.move_to_element(textBox).send_keys(ingredient[1], Keys.RETURN)
            
            textBox.send_keys(ingredient[1])
            '''
            textBox.send_keys(Keys.TAB)
            actions = ActionChains(driverTandoori)
            #actions.send_keys(titlecase(ingredient[1]))
            actions.send_keys(ingredient[1])
            actions.send_keys(Keys.ENTER)
            actions.perform()

            time.sleep(.3)

            # food
            #textBox.send_keys(Keys.TAB)
            actions = ActionChains(driverTandoori)
            actions.send_keys(Keys.TAB)
            actions.send_keys(ingredient[2])
            print('ingredient entering name ' + str(ingredient[2]))
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(.3)

            row = row + 1
    if (recipeObject["calories"] != None) and (recipeObject["calories"] != 0):
        # trying to press the add nutrition button
        addNutrition = driverTandoori.find_element_by_xpath('//div[@class="col-md-3"]')
        addNutrition = addNutrition.find_element_by_tag_name('button').click()

        calories = driverTandoori.find_element_by_xpath('//input[@id="id_calories"]')
        calories.send_keys(recipeObject["calories"])

        carbs = driverTandoori.find_element_by_xpath('//input[@id="id_carbohydrates"]')
        carbs.send_keys(recipeObject["carbs"])

        fats = driverTandoori.find_element_by_xpath('//input[@id="id_fats"]')
        fats.send_keys(recipeObject["fats"])

        proteins = driverTandoori.find_element_by_xpath('//input[@id="id_proteins"]')
        proteins.send_keys(recipeObject["proteins"])

def bonappetit(driver, recipeLink, recipeObject):
    driver.get(recipeLink)
    time.sleep(1)

    # url
    recipeObject["url"] = recipeLink

    # getting the image
    try:
        image = driver.find_element_by_xpath('//img[contains(@src, "https://assets.bonappetit.com/photos/")]')
        image = image.get_attribute('src')
        print('image url = ' + str(image))
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        print('No image')
        recipeObject["image"] = None

    # title
    recipeObject['title'] = driver.find_element_by_xpath('//h1[@data-testid="ContentHeaderHed"]').get_attribute("innerHTML")

    # description
    try:
        recipeObject['description'] = driver.find_element_by_xpath('//div[@class="container--body-inner"]').text
    except:
        recipeObject['description'] = ""

    # author
    try:
        recipeObject['author'] = titlecase(driver.find_element_by_xpath('//a[contains(@href, "/contributor/")]').text) + ' for Bon Appetit'
    except:
        recipeObject['author'] = 'The Bon Appetit Test Kitchen'

    # serving amount
    try:
        recipeObject['servingsAmount'] = driver.find_element_by_xpath('//p[@class="BaseWrap-sc-TURhJ BaseText-fFzBQt Yield-hqywEg eTiIvU cpiNFi bMptcf"]').text
        recipeObject['servingsAmount'] = [int(x) for x in recipeObject['servingsAmount'].split() if x.isdigit()][0]
    except:
        pass

    # serving unit
    try:
        recipeObject['servingsUnit'] = driver.find_element_by_xpath('//p[@class="BaseWrap-sc-TURhJ BaseText-fFzBQt Yield-hqywEg eTiIvU cpiNFi bMptcf"]').text
        recipeObject['servingsUnit'] = titlecase(''.join([i for i in recipeObject['servingsUnit'] if not i.isdigit()]))
    except:
        pass

    # active time

    # waiting time

    # steps
    for step in driver.find_elements_by_xpath('//div[contains(@class, "BaseWrap-sc-TURhJ BaseText-fFzBQt InstructionBody-hvjmoZ")]'):
        print('step: ' + str(step.text))
        recipeObject["steps"].append(step.text)


    # ingredients
    # [AMOUNT OF INGRED, UNIT OF INGRED, INGRED NAME]

    #row = 0

    # for each ingredient (row)
    row = 0
    for item in driver.find_elements_by_xpath('//p[contains(@class, "BaseWrap-sc-TURhJ BaseText-fFzBQt Amount-")]'):

        recipeIngredient = driver.find_elements_by_xpath('//p[contains(@class, "BaseWrap-sc-TURhJ BaseText-fFzBQt Amount-VUCfl")]')[row].text + ' ' + driver.find_elements_by_xpath('//div[contains(@class, "BaseWrap-sc-TURhJ BaseText-fFzBQt Description-dSNklj")]')[row].text

        recipeIngredient, prep = ingredientFilter.main(textToIngredient(recipeIngredient), None)

        recipeObject["ingredients"].append( recipeIngredient )
        for prepItem in prep:
            recipeObject["prep"].append(prepItem)
            
        row += 1



        '''recipeIngredient = [0, "NO_UNIT", ""]
        ingredientAmount = driver.find_elements_by_xpath('//p[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Amount-Wcygw hlNbBe dNHZzc jpdXhZ"]')[row]
        ingredientName = driver.find_elements_by_xpath('//div[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Description-dSowHq hlNbBe dNHZzc eRguAM"]')[row]

        # get the ammount
        try:
            recipeIngredient[0] = float(ingredientAmount.get_attribute("innerHTML"))
        except: # if there is a unicode fraction in the ingred list
            try:
                recipeIngredient[0] = fracCharToFloat(ingredientAmount.get_attribute("innerHTML"))
            except:
                recipeIngredient[0] = 0.000

        # get the name
        recipeIngredient[2] = ingredientName.text

        recipeIngredient, prep = ingredientFilter.main(recipeIngredient, None)

        recipeObject["ingredients"].append(recipeIngredient)

        row += 1'''


    '''for prepItem in prep:
        recipeObject["prep"].append(prepItem)'''

    print(
        '\nURL: '           + recipeObject["url"] + 
        '\nTitle: '         + recipeObject["title"] + 
        '\nActive Time: '   + str(recipeObject["timeActive"]) + 
        '\nWaiting Time: '  + str(recipeObject["timeWaiting"]) + 
        '\nServings: '      + str(recipeObject["servingsAmount"]) + ' ' + recipeObject["servingsUnit"] + 
        '\nAuthor: '        + recipeObject["author"] + 
        '\nIngredients: '   + str(recipeObject["ingredients"]) + 
        '\nCalories: '      + str(recipeObject["calories"]) + 
        '\nCarbs: '         + str(recipeObject["carbs"]) +
        '\nFats: '          + str(recipeObject["fats"]) + 
        '\nProteins: '      + str(recipeObject["proteins"]) + 
        '\nDescription: '   + recipeObject["description"] + 
        '\nSteps: '         + str(recipeObject["steps"]) + 
        '\nPrep: '          + str(recipeObject["prep"]) + 
        '\nTips: '          + str(recipeObject["tips"]) + 
        '\nTags: '          + str(recipeObject["tags"])
    )


    # prep

    return(recipeObject)

def simplyrecipes(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # url
    recipeObject['url'] = recipeLink

    # title
    recipeObject['title'] = driver.find_element_by_xpath('//h1[@class="heading__title"]').text

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="primary-image mntl-primary-image figure__image js-figure-image mntl-primary-image--blurry loaded"]')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.webp")
        image = Image.open('recipe.webp').convert("RGB")
        image.save('recipe.png', 'png')
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # author
    recipeObject['author'] = titlecase( driver.find_element_by_xpath('//a[@id="mntl-byline__link_1-0"]').text )

    # description
    recipeObject['description'] = driver.find_element_by_xpath('//h2[@class="heading__subtitle"]').text

    # serving amount
    recipeObject['servingsAmount'] = driver.find_element_by_xpath('//span[@id="meta-text_5-0"]')
    recipeObject['servingsAmount'] = recipeObject['servingsAmount'].find_element_by_xpath('//span[@class="meta-text__data"]').text
    recipeObject['servingsAmount'] = [int(x) for x in recipeObject['servingsAmount'].split() if x.isdigit()][0]

    # serving unit
    recipeObject['servingsUnit'] = driver.find_element_by_xpath('//div[@class="loc recipe-yield project-meta__recipe-yield"]')

    recipeObject['servingsUnit'] = recipeObject['servingsUnit'].find_element_by_xpath('.//span[@id="meta-text_5-0"]')

    recipeObject['servingsUnit'] = recipeObject['servingsUnit'].find_element_by_xpath('.//span[@class="meta-text__data"]').text

    print(str(recipeObject['servingsUnit']))

    recipeObject['servingsUnit'] = str(titlecase(''.join([i for i in recipeObject['servingsUnit'] if not i.isdigit()])[1:]))
    

    
    # active time
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="loc prep-time project-meta__prep-time"]')
    recipeObject["timeActive"] = driver.find_element_by_xpath('.//span[@id="meta-text_2-0"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('.//span[@class="meta-text__data"]').text

    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])

    #recipeObject['timeActive'] = [int(x) for x in recipeObject['servingsAmount'].split() if x.isdigit()][0]


    # waiting time
    try:
        recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="loc cook-time project-meta__cook-time"]')
        recipeObject["timeWaiting"] = driver.find_element_by_xpath('.//span[@id="meta-text_3-0"]')
        recipeObject["timeWaiting"] = recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="meta-text__data"]').text

        recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])

        print('TEXT TIME: ' + str(recipeObject["timeWaiting"]))
    except:
        recipeObject["timeWaiting"] = 0


    # steps
    
    for step in driver.find_elements_by_xpath('//li[@class="comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup"]'):
        recipeObject["steps"].append(step.text)

    # ingredients
    # [AMOUNT OF INGRED, UNIT OF INGRED, INGRED NAME]
    for ingredient in driver.find_elements_by_xpath('//li[@class="simple-list__item js-checkbox-trigger ingredient text-passage"]'):
        '''
        nb_rep = 1
        s = ingredient.text
        while (nb_rep):
            (s, nb_rep) = re.subn(r'\([^()]*\)', '', s)

        ingredient = s

        ingredient = re.sub('[\(\[].*?[\)\]]', "", ingredient)
        ingredient = re.sub(' +', ' ', ingredient)
        recipeObject["ingredients"] = ingredient.split()
        print('ingredient = ' + str(float(recipeObject["ingredients"][0])) + recipeObject['ingredients'][1] + recipeObject['ingredients'][2] +'\n')
        '''
        textToIngredient(ingredient.text)
        recipeObject["ingredients"].append(textToIngredient(ingredient.text))

    # prep

    # tags

    # calories

    # carbs

    # fats

    # proteins

    # tips

    # printout

    return(recipeObject)
    
def epicurious(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:


        image = driver.find_element_by_xpath('//img[@class="responsive-image__image" and contains(@src, "/photos/")]')
        #image = driver.find_element_by_xpath('//img[contains]')
        image = image.get_attribute('src')
        print(image)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.webp', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
        '''
        image = driver.find_element_by_xpath('//img[@class="responsive-image__image"]')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.jpg")
        '''
        image = Image.open('./recipe.webp')
        image.save('./recipe.png')

        recipeObject["image"] = True



        '''
        image = driver.find_element_by_xpath('//img[@class="responsive-image__image"]')
        image = image.get_attribute('srcset')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
        '''
    except Exception as e:
        print('Failed to download photo: ' + str(e))
        recipeObject["image"] = None

    # url
    recipeObject['url'] = recipeLink

    # title
    try:
        recipeObject['title'] = str(driver.find_element_by_xpath('//h1[@itemprop="name"]').text)
    except:
        recipeObject['title'] = str(driver.find_element_by_xpath('//h1[@data-testid="ContentHeaderHed"]').text)
    print('Title = ' + str(recipeObject['title']))

    # time active
    try:
        recipeObject["timeActive"] = driver.find_element_by_xpath('//dd[@class="active-time"]').text
        recipeObject["timeActive"] = textTime(recipeObject["timeActive"])
        print('active time = ' + str(recipeObject["timeActive"]))
    except:
        recipeObject["timeActive"] = 0

    # time waiting
    try:
        recipeObject["timeWaiting"] =  driver.find_element_by_xpath('//dd[@class="total-time"]').text
        recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])
        recipeObject["timeWaiting"] = recipeObject["timeWaiting"] - recipeObject["timeActive"]
        print('waiting time = ' + str(recipeObject["timeActive"]))
    except:
        recipeObject["timeWaiting"] = 0


    # servings amount
    try:
        servings = driver.find_element_by_xpath('//p[contains(@class, "Yield-")]').text
        servings = re.sub("[^0-9]", "", servings)
        recipeObject["servingsAmount"] = servings
    except:
        recipeObject["servingsAmount"] = 1

    # servings unit
    recipeObject["servingsUnit"] = "Servings"

    # author
    try:
        author = driver.find_element_by_xpath('//a[contains(@class, "byline__name-link")]').text
        recipeObject["author"] = titlecase(author) + ' for Epicurious.com'
    except:
        recipeObject["author"] = "Epicurious.com"

    # ingredients
    prep = []
    foundEngredients = driver.find_element_by_xpath('//div[contains(@class, "List-")]')
    foundEngredients = foundEngredients.find_elements_by_xpath('.//div[contains(@class, " Description-")]')
    if len(foundEngredients) > 0:
        for ingredient in foundEngredients:
            tempIngredient = textToIngredient(ingredient.text)
            print('found ingredients' + str(tempIngredient))
            tempIngredient, prep = ingredientFilter.main(tempIngredient, prep)

            recipeObject["ingredients"].append(tempIngredient)
    else:
        box = driver.find_element_by_xpath('//div[contains(@class, "List-")]')

        amounts = []
        titles  = []


        for amount in box.find_elements_by_xpath('.//div[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Amount-Wcygw hlNbBe dZgHQP jpdXhZ"]'):

            try:
                amounts.append(amount.text)
            except:
                amounts.append(' ')

        for title in box.find_elements_by_xpath('.//div[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Description-dSowHq hlNbBe dZgHQP eRguAM"]'):

            try:
                titles.append(title.text)
            except:
                titles.append(' ')

        allIngredients = []
        index = 0
        for line in titles:

            line = amounts[index] + ' ' + titles[index]
            line = re.sub(' +', ' ', line)
            print('1. line = ' + str(line))
            line = textToIngredient(line)
            print('2. line = ' + str(line))
            #line, prep = textToIngredient(line, prep)
            line, prep = ingredientFilter.main(line, prep)


            #amount = box.find_element_by_xpath('.//p[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Amount-Wcygw hlNbBe dZgHQP jpdXhZ"]').text
            #title  = box.find_element_by_xpath('.//div[@class="BaseWrap-sc-TwdDQ BaseText-fFHxRE Description-dSowHq hlNbBe dZgHQP eRguAM"]').text
            '''
            line = amount + ' ' + title
            line = re.sub(' +', ' ', line)
            print('1. line = ' + str(line))
            line = textToIngredient(line)
            print('2. line = ' + str(line))
            #line, prep = textToIngredient(line, prep)
            line, prep = ingredientFilter.main(line, prep)
            #print('3. line = ' + str(line))
            '''
            recipeObject["ingredients"].append(line)
            index += 1

    # calories

    # carbs

    # fats

    # proteins

    # description
    try:
        recipeObject["description"] = driver.find_element_by_xpath('//div[@class="container--body-inner"]').text
    except:
        recipeObject["description"] = ""

    # steps
    for step in driver.find_elements_by_xpath('//div[contains(@class, "InstructionBody-")]'):
        recipeObject["steps"].append(step.text)

    # prep
    for item in prep:
        recipeObject["prep"].append(item)

    # tips

    # tags

    return(recipeObject)

def altonBrown(driver, recipeLink, recipeObject):
    driver.get(recipeLink)
    time.sleep(1)

    #recipeObject = recipe()

    ### Initialize

    recipeObject["url"] = recipeLink

    ### Image
    try:
        image = driver.find_element_by_class_name('wprm-recipe-image')
        image = image.find_element_by_tag_name('img')

        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    ### Title

    recipeObject["title"] = titlecase(str(driver.find_element_by_class_name('wprm-recipe-name').text))

    ### Description
    try:
        recipeObject["description"] = driver.find_element_by_class_name('wprm-recipe-summary')
        recipeObject["description"] = recipeObject["description"].find_element_by_tag_name('span').get_attribute("innerHTML")
    except:
        recipeObject["description"] = ""

    ### Author

    recipeObject["author"] = 'Alton Brown'

    ### Servings

    recipeObject["servingsAmount"] = driver.find_element_by_class_name('wprm-recipe-servings').get_attribute("innerHTML")

    try:
        recipeObject["servingsUnit"] = titlecase(driver.find_element_by_class_name('wprm-recipe-servings-unit').get_attribute("innerHTML"))
    except:
        recipeObject["servingsUnit"] = "Servings"

    ### Active Time

    recipeObject["timeActive"] = 0

    try:
        recipeObject["timeActive"] += int(driver.find_element_by_class_name('wprm-recipe-prep_time-hours').get_attribute("innerHTML")) * 60
    except:
        pass

    try:
        recipeObject["timeActive"] += int(driver.find_element_by_class_name('wprm-recipe-prep_time-minutes').get_attribute("innerHTML"))
    except:
        pass

    ### Waiting Time

    recipeObject["timeWaiting"] = 0

    try:
        recipeObject["timeWaiting"] += int(driver.find_element_by_class_name('wprm-recipe-total_time-hours').get_attribute("innerHTML")) * 60
    except:
        pass

    try:
        recipeObject["timeWaiting"] += int(driver.find_element_by_class_name('wprm-recipe-total_time-minutes').get_attribute("innerHTML"))
    except:
        pass

    recipeObject["timeWaiting"] = recipeObject["timeWaiting"] - recipeObject["timeActive"]

    ### Steps
    try:
        for step in driver.find_elements_by_class_name("wprm-recipe-instruction"):
            recipeObject["steps"].append(step.text)
            #print(step.text)
    except:
        pass

    ### Ingredients
    # [AMOUNT OF INGRED, UNIT OF INGRED, INGRED NAME]

    #recipeObject["ingredients"] = recipeObject["ingredients"].clear()

    for ingredient in driver.find_elements_by_class_name("wprm-recipe-ingredient"):
        recipeIngredient = []
        
        try:    # AMOUNT
            recipeIngredient.append(convertToFloat(ingredient.find_element_by_class_name('wprm-recipe-ingredient-amount').get_attribute("innerHTML")))
        except:
            recipeIngredient.append(0)

        try:    # UNIT
            recipeIngredient.append(titlecase(ingredient.find_element_by_class_name('wprm-recipe-ingredient-unit').text))
        except:
            recipeIngredient.append('Count')

        try:    # NAME
            recipeIngredient.append(titlecase(ingredient.find_element_by_class_name('wprm-recipe-ingredient-name').text))
        except:
            pass

        recipeIngredient, prep = ingredientFilter.main(recipeIngredient, None)

        recipeObject["ingredients"].append(recipeIngredient)

        for prepItem in prep:
            recipeObject["prep"].append(prepItem)


    ## this is where prep would go

    return(recipeObject)

def sbs(driver, recipeLink, recipeObject):
    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//div[@class="media-item field_image  on"]')
        image = image.find_element_by_tag_name('img')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@class="title"]').text)

    # time active
    try:
        recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="field field-name-field-preparation-time field-type-number-integer field-label-above"]')
        recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('.//span[@class="value"]').text
        recipeObject["timeActive"] = int(recipeObject["timeActive"])
    except:
        recipeObject["timeActive"] = 0

    # time waiting
    
    #recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[class="field field-name-field-cooking-time field-type-number-integer field-label-above"]')
    
    minutesTotal = 0

        # trying to get hours
    try:
        hours = driver.find_element_by_xpath('//div[@class="field field-name-field-cooking-time field-type-number-integer field-label-above"')
        hours = hours.find_element_by_xpath('.//div[@class="timeperiod-hr"]')
        hours = hours.find_element_by_xpath('.//span[@class="value"]').text
        minutesTotal = (60 * int(hours))
    except:
        pass

        # getting minutes

    try:
        minutes = driver.find_element_by_xpath('//div[@class="field field-name-field-cooking-time field-type-number-integer field-label-above"]')
        minutes = minutes.find_element_by_xpath('.//div[@class="timeperiod-min"]')
        minutes = minutes.find_element_by_xpath('.//span[@class="value"]').text

        minutesTotal += int(minutes)
    except:
        pass

    recipeObject["timeWaiting"] = minutesTotal

    # serving amount
    try:
        recipeObject["servingsAmount"] = int(driver.find_element_by_xpath('//div[@class="field field-name-field-serving-size field-type-text field-label-hidden"]').text)
    except:
        recipeObject["servingsAmount"] = 0

    # serving unit
    recipeObject["servingsUnit"] = "Servings"

    # author

    recipeObject["author"] = titlecase(driver.find_element_by_xpath('//div[@itemprop="author"]').text + ' for sbs.com.au')

    # ingredients
    prep = []

    ingredients = driver.find_element_by_xpath('//div[@class="field field-recipe-ingredients"]')
    #ingredients = ingredients.find_element_by_tag_name('ul')
    ingredients = ingredients.find_elements_by_tag_name('li')

    for ingredient in ingredients:

        convertedIngredient = textToIngredient(ingredient.text)

        # [amount, unit, name]
        # since this is from australia
        # and australia uses DIFFERENT
        # tablespoons and tespoons and stuff
        # than america (or england for that matter)
        # i gotta see if any of these ingredients
        # are weird australian units
        # these conversions are from the sbs
        # cooks notes 

        print('sbs ingredient ' + str(convertedIngredient))

        if 'tablespoon' in (convertedIngredient[1].lower()):
            print('converting to metric')
            convertedIngredient[1] = 'Milliliters'
            convertedIngredient[0] = float(convertedIngredient[0] * 20)
        elif 'teaspoon' in (convertedIngredient[1].lower()):
            print('converting to metric')
            convertedIngredient[1] = 'Milliliters'
            convertedIngredient[0] = float(convertedIngredient[0] * 5)
        elif 'cup' in (convertedIngredient[1].lower()):
            print('converting to metric')
            convertedIngredient[1] = 'Milliliters'
            convertedIngredient[0] = float(convertedIngredient[0] * 250)

        convertedIngredient, prep = ingredientFilter.main(convertedIngredient, prep)

        recipeObject["ingredients"].append(convertedIngredient)

    # calories

    # carbs

    # fats

    # proteins

    # description

    # steps

    steps = driver.find_element_by_xpath('//div[@class="field field-name-field-cooking-instructions field-type-text-long field-label-hidden cXenseParse"]')
    steps = steps.find_elements_by_tag_name('p')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep
    for item in prep:
        recipeObject["prep"].append(item)

    # tips

    # tags

    return recipeObject

def woksOfLife(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="attachment-post-thumbnail size-post-thumbnail wp-post-image lazyloaded"]')
        #image = image.find_element_by_tag_name('img')
        image = image.get_attribute('src')
        print(image)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.png', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
        #urllib.request.urlretrieve(image, "recipe.png")
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h2[@class="wprm-recipe-name wprm-block-text-normal"]').text)

    # time active
    recipeObject["timeActive"] = 0

    try:        # get hours, if any
        recipeObject["timeActive"] += int(driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-details-hours wprm-recipe-prep_time wprm-recipe-prep_time-hours"]').text) * 60
    except:
        pass

    try:        # get minutes, if any
        recipeObject["timeActive"] += int(driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes"]').text)
    except:
        pass

    # time waiting
    recipeObject["timeWaiting"] = 0

    try:        # get hours, if any
        recipeObject["timeWaiting"] += int(driver.find_elements_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-details-hours wprm-recipe-cook_time wprm-recipe-cook_time-hours"]').text) * 60
    except:
        pass

    try:        # get minutes, if any
         recipeObject["timeWaiting"] += int(driver.find_elements_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes"]').text)
    except:
        pass

    # serving amount
        # i know this is fucked,
        # but, it cannot find the tag where the number is stored
        # but it can find its parent
        # so i find the text of the parent and
        # remove all non numbers
    amount = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal wprm-recipe-servings-container"]').text
    amount =  re.sub("[^0-9]", "", amount)
    recipeObject["servingsAmount"] = int(amount)

    # serving unit
    recipeObject["servingsUnit"] = "Servings"

    # author
    recipeObject["author"] = 'The Woks of Life'

    # ingredients
    # [amount, unit, name]
    lines = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')

    for line in lines:
        ingredient = [0.000, "", ""]

        print(line.text)

        # this site uses BOTH unicode charactars for fractions and typed out fractions
        try:
            ingredient[0] = convertToFloat(line.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text)
        except NoSuchElementException:
            ingredient[0] = 0.000
        except: 
            ingredient[0] = fracCharToFloat(line.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text)


        try:
            ingredient[1] = titlecase(line.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-unit"]').text)
        except:
            ingredient[1] = 'Count'

        ingredient[2] = titlecase(line.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-name"]').text)

        recipeObject["ingredients"].append(ingredient)

    # calories

    # carbs

    # carbs

    # fats

    # proteins

    # description

    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]').text

    # steps

    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

def seriousEats(driver, recipeLink, recipeObject):
    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="primary-image mntl-primary-image figure__image js-figure-image mntl-primary-image--blurry loaded"]')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.webp")
        image = Image.open('recipe.webp').convert("RGB")
        image.save('recipe.png', 'png')
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@class="heading__title"]').text)

    # time active
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="loc active-time project-meta__active-time"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('.//span[@class="meta-text__data"]').text
    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])
    #recipeObject["timeActive"] = int(re.sub("[^0-9]", "", recipeObject["timeActive"]))

    # time waiting
    recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="loc total-time project-meta__total-time"]')
    recipeObject["timeWaiting"] = recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="meta-text__data"]').text
    recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])
    #recipeObject["timeWaiting"] = int(re.sub("[^0-9]", "", recipeObject["timeWaiting"]))
    recipeObject["timeWaiting"] = recipeObject["timeWaiting"] - recipeObject["timeActive"]

    # serving amount
    try:
        try:
            recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="loc recipe-yield project-meta__recipe-yield"]')
        except:
            recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="loc recipe-serving project-meta__recipe-serving"]')
        recipeObject["servingsAmount"] = recipeObject["servingsAmount"].find_element_by_xpath('.//span[@class="meta-text__data"]').text
        recipeObject["servingsAmount"] = int(re.sub("[^0-9]", "", recipeObject["servingsAmount"]))
    except:
        recipeObject["servingsAmount"] = 1

    # serving unit
    try:
        try:
            recipeObject["servingsUnit"] = driver.find_element_by_xpath('//div[@class="loc recipe-yield project-meta__recipe-yield"]')
        except:
            recipeObject["servingsUnit"] = driver.find_element_by_xpath('//div[@class="loc recipe-serving project-meta__recipe-serving"]')
        recipeObject["servingsUnit"] = recipeObject["servingsUnit"].find_element_by_xpath('.//span[@class="meta-text__data"]').text
        recipeObject["servingsUnit"] = titlecase(re.sub(r'\d+', '', recipeObject["servingsUnit"]))
    except:
        recipeObject["servingsUnit"] = 'Servings'

    # author
    recipeObject["author"] = driver.find_element_by_xpath('//a[@class="mntl-attribution__item-name"]').text + ' for Serious Eats'

    # ingredients
    prep = []
    ingredients = driver.find_elements_by_xpath('//li[@class="simple-list__item js-checkbox-trigger ingredient text-passage"]')

    for ingredient in ingredients:
        ingredient = textToIngredient(ingredient.text)
        ingredient, prep = ingredientFilter.main(ingredient, prep)
        recipeObject["ingredients"].append(ingredient)

    # calories

    # carbs

    # fats

    # proteins

    # description

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup"]')

    for step in steps:
        recipeObject["steps"].append(step.text)
    
    # prep
    for item in prep:
        item = re.sub(' +', ' ', item)
        recipeObject["prep"].append(item)

    # tips

    # tags

    return recipeObject

def food52(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # url
    recipeObject["url"] = recipeLink

    # image
    try:
        image = driver.find_element_by_xpath('//a[@class="img__pin"]')
        image = image.get_attribute('data-pin-media')
        print(image)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.webp', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    image = Image.open('recipe.webp').convert("RGB")
    image.save('recipe.png', 'png')

    # title
    recipeObject["title"] = driver.find_element_by_xpath('//h1[@class="recipe__title"]').text

    # time active
    recipeObject["timeActive"] = driver.find_element_by_xpath('//ul[@class="recipe__details"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_elements_by_tag_name('li')[0].text.lower().replace('prep time', '')
    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])


    # time waiting
    recipeObject["timeWaiting"] = driver.find_element_by_xpath('//ul[@class="recipe__details"]')
    recipeObject["timeWaiting"] = recipeObject["timeWaiting"].find_elements_by_tag_name('li')[1].text.lower().replace('cook time', '')
    recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])

    # serving amount
    '''
    pseudocode
    the amount is the string
    with all the non numeric chars removed

    for the unit,
    remove all the numeric chars
    whats left is the unit

    If the unit is "serves"
    change it to servings
    '''
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//ul[@class="recipe__details"]')
    recipeObject["servingsAmount"] = recipeObject["servingsAmount"].find_elements_by_tag_name('li')[2].text
    recipeObject["servingsAmount"] = re.sub('[^0-9]','', recipeObject["servingsAmount"])

    # serving unit
    recipeObject["servingsUnit"] = driver.find_element_by_xpath('//ul[@class="recipe__details"]')
    recipeObject["servingsUnit"] = recipeObject["servingsUnit"].find_elements_by_tag_name('li')[2].text
    recipeObject["servingsUnit"] = titlecase(re.sub(r'\d+', '', recipeObject["servingsUnit"]))
    if str(recipeObject["servingsUnit"]).lower() == 'serves':
        print('THE SERVING UNIT IS NOT SERVES')
    else:
        recipeObject["servingsUnit"] = "Servings"
        print('NO LONGER SERVES')


    # author
    '''
    food52 does a thing like
    "firstname lastname | stuff stuffy"
    so imma thinking that i split it by " | "
    then just set author to be [0] of the array
    '''
    recipeObject["author"] = driver.find_element_by_xpath('//div[@class="meta__author"]')
    recipeObject["author"] = titlecase(recipeObject["author"].find_element_by_tag_name('a').text.split(' | ')[0])


    # ingredients
    ingredients = driver.find_element_by_xpath('//div[@class="recipe__list recipe__list--ingredients"]')
    ingredients = ingredients.find_elements_by_tag_name('li')

    # because the first element is a header
    #ingredients.pop(0)

    for ingredient in ingredients:

        try:
            if ingredient.get_attribute('class') == 'recipe__list-subheading':
                pass
            else:
                recipeObject["ingredients"].append(textToIngredient(ingredient.text))
        except:
            pass

    # calories

    # carbs

    # fats

    # proteins

    # description

    # steps
    steps = driver.find_element_by_xpath('//div[@class="recipe__list recipe__list--steps"]')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

'''
print(
    '\nURL: '           + recipeObject["url"] + 
    '\nTitle: '         + recipeObject["title"] + 
    '\nActive Time: '   + str(recipeObject["timeActive"]) + 
    '\nWaiting Time: '  + str(recipeObject["timeWaiting"]) + 
    '\nServings: '      + str(recipeObject["servingsAmount"]) + ' ' + recipeObject["servingsUnit"] + 
    '\nAuthor: '        + recipeObject["author"] + 
    '\nIngredients: '   + str(recipeObject["ingredients"]) + 
    '\nCalories: '      + str(recipeObject["calories"]) + 
    '\nCarbs: '         + str(recipeObject["carbs"]) +
    '\nFats: '          + str(recipeObject["fats"]) + 
    '\nProteins: '      + str(recipeObject["proteins"]) + 
    '\nDescription: '   + recipeObject["description"] + 
    '\nSteps: '         + str(recipeObject["steps"]) + 
    '\nPrep: '          + str(recipeObject["prep"]) + 
    '\nTips: '          + str(recipeObject["tips"]) + 
    '\nTags: '          + str(recipeObject["tags"])
)
'''

def budgetBytes(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(5)

    # image
    image = driver.find_element_by_xpath('//article[@class="post single-post single-post-content"]')
    image = image.find_element_by_xpath('.//div[contains(@class, "dpsp-pin-it-wrapper alignnone wp-image")]')
    image = image.find_element_by_tag_name('img').get_attribute('src')
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
    }
    request_ = urllib.request.Request(image, None, headers)
    response = urllib.request.urlopen(request_)
    f = open('recipe.png', 'wb')
    f.write(response.read())
    f.close()
    recipeObject["image"] = True

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h2[@class="wprm-recipe-name wprm-block-text-bold"]').text)

    # active time
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal wprm-recipe-time-container wprm-recipe-prep-time-container"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])

    # waiting time
    recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal wprm-recipe-time-container wprm-recipe-cook-time-container"]')
    recipeObject["timeWaiting"] =  recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])

    # serving amount
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal wprm-recipe-servings-container"]')
    recipeObject["servingsAmount"] = int(recipeObject["servingsAmount"].find_element_by_tag_name('input').get_attribute('value'))


    # serving unit 
    recipeObject["servingsUnit"] = "Servings"

    # author
    recipeObject["author"] = 'Beth of Budget Bytes'

    # ingredients
    # ingredients
    prep = []
    ingredients = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')
    for ingredient in ingredients:
        ingredientWorking = [0.000, "", ""]

       # amount
        try:
            ingredientWorking[0] = ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text
        except:
            ingredientWorking[0] = 0.000

        # trying to make it float, assuming it is an easy conversion
        try:
            ingredientWorking[0] = float(ingredientWorking[0])
        except ValueError:
            # is the amount a frac char?
            try:
                ingredientWorking[0] = fracCharToFloat(ingredientWorking[0])
            except:
                try:
                    # it is a string fractions
                    ingredientWorking[0] = convertToFloat(ingredientWorking[0])
                except:
                    ingredientWorking[0] = ingredientWorking[0].split('-')
                    ingredientWorking[0] = (float(ingredientWorking[0][0]) + float(ingredientWorking[0][1])) / 2
        except:
            ingredientWorking[0] = 0.000

        # unit
        try:
            ingredientWorking[1] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-unit"]').text)

            if (str(ingredientWorking[1]).lower()) == 'g':
                ingredientWorking[1] = 'Grams'
            elif (str(ingredientWorking[1]).lower()) == 'ml':
                ingredientWorking[1] = 'Milliliters'
            elif (str(ingredientWorking[1]).lower()) == 'kg':
                ingredientWorking[1] = 'Kilograms'
            elif (str(ingredientWorking[1]).lower()) == 'tbs':
                ingredientWorking[1] = 'Tablespoon'
            elif (str(ingredientWorking[1]).lower()) == 'tbsp':
                ingredientWorking[1] = 'Tablespoon'
            elif (str(ingredientWorking[1]).lower()) == 'tsp':
                ingredientWorking[1] = 'Teaspoon'
            elif (str(ingredientWorking[1]).lower()) == 'lb':
                ingredientWorking[1] = 'Pounds'
            elif (str(ingredientWorking[1]).lower()) == 'oz':
                ingredientWorking[1] = 'Ounces'
        except:
            ingredientWorking[1] = 'Count'

        # name
        ingredientWorking[2] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-name"]').text)

        ingredientWorking, prep = ingredientFilter.main(ingredientWorking, prep)

        recipeObject["ingredients"].append(ingredientWorking)

    # calories
    nutrition = driver.find_elements_by_xpath('//span[@class="wprm-nutrition-label-text-nutrition-value"]')
    recipeObject["calories"] = (nutrition[1].text)

    # carbs
    recipeObject["carbs"] = (nutrition[2].text)

    # fats
    recipeObject["fats"] = (nutrition[4].text)

    # protiens
    recipeObject["proteins"] = (nutrition[3].text)

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]').text

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')
    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep
    for item in prep:
        recipeObject["prep"].append(item)

    # tips

    # tags

    return recipeObject

def veganRicha(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        #image = driver.find_element_by_xpath('//img[contains(@class, "alignnone size-full wp-")]').get_attribute('src')
        image = driver.find_element_by_xpath('//img[@data-jpibfi-post-url="' + recipeLink + '"]').get_attribute('src')
        #image = driver.find_element_by_xpath('//img[@class="alignnone lazyloaded"]').get_attribute('src')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.png', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = str(recipeLink)

    # title
    recipeObject["title"] = titlecase(str(driver.find_element_by_xpath('//h2[@class="wprm-recipe-name wprm-block-text-bold"]').text))

    # active time
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-table wprm-block-text-normal wprm-recipe-time-container wprm-recipe-prep-time-container"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeActive"] = int(textTime(recipeObject["timeActive"]))

    # waiting time
    recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-table wprm-block-text-normal wprm-recipe-time-container wprm-recipe-cook-time-container"]')
    recipeObject["timeWaiting"] = recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeWaiting"] = int(textTime(recipeObject["timeWaiting"]))

    # servings amount
    servings = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-inline wprm-block-text-bold wprm-recipe-servings-container"]')
    recipeObject["servingsAmount"] = servings.find_element_by_tag_name('input')
    recipeObject["servingsAmount"] = int(recipeObject["servingsAmount"].get_attribute('value'))

    # serving unit
    try:
        recipeObject["servingsUnit"] = servings.find_element_by_xpath('.//span[@class="wprm-recipe-servings-with-unit"]')
        recipeObject["servingsUnit"] = titlecase(recipeObject["servingsUnit"].find_element_by_xpath('.//span[@class="wprm-recipe-servings-unit wprm-recipe-details-unit wprm-block-text-bold"]').text)
    except:
        recipeObject["servingsUnit"] = "Servings"

    # author
    recipeObject["author"] = titlecase(driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-author wprm-block-text-normal"]').text)

    # ingredients
    ingredients = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')
    prep = []
    for ingredient in ingredients:
        '''
        ingredientWorking = [0.000, "", ""]
        try:
            # amount
            try:
                ingredientWorking[0] = ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text
            except:
                ingredientWorking[0] = 0.000

            # trying to make it float, assuming it is an easy conversion
            try:
                ingredientWorking[0] = float(ingredientWorking[0])
            except ValueError:
                # is the amount a frac char?
                try:
                    ingredientWorking[0] = fracCharToFloat(ingredientWorking[0])
                except:
                    # it is a string fractions
                    ingredientWorking[0] = convertToFloat(ingredientWorking[0])

            except:
                ingredientWorking[0] = 0.000

            # unit
            try:
                ingredientWorking[1] = ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-unit"]').text

                if (str(ingredientWorking[1]).lower()) == 'g':
                    ingredientWorking[1] = 'Grams'
                elif (str(ingredientWorking[1]).lower()) == 'ml':
                    ingredientWorking[1] = 'Milliliters'
                elif (str(ingredientWorking[1]).lower()) == 'kg':
                    ingredientWorking[1] = 'Kilograms'
                elif (str(ingredientWorking[1]).lower()) == 'tbs':
                    ingredientWorking[1] = 'Tablespoon'
                elif (str(ingredientWorking[1]).lower()) == 'tbsp':
                    ingredientWorking[1] = 'Tablespoon'
                elif (str(ingredientWorking[1]).lower()) == 'tsp':
                    ingredientWorking[1] = 'Teaspoon'
                elif (str(ingredientWorking[1]).lower()) == 'lb':
                    ingredientWorking[1] = 'Pounds'
                elif (str(ingredientWorking[1]).lower()) == 'oz':
                    ingredientWorking[1] = 'Ounces'
            except:
                ingredientWorking[1] = 'Count'

            # name
            ingredientWorking[2] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-name"]').text)
        except:
            ingredientWorking = textToIngredient(ingredient.text)
        '''
        ingredientWorking = textToIngredient(ingredient.text)
        ingredientWorking, prep = ingredientFilter.main(ingredientWorking, prep)

        recipeObject["ingredients"].append(ingredientWorking)

    # calories
    recipeObject["calories"] = int( driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal"]').text )

    # carbs
    recipeObject["carbs"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-carbohydrates"]')
    recipeObject["carbs"] = recipeObject["carbs"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["carbs"] = re.sub("[^0-9]", "", recipeObject["carbs"])

    # fats
    recipeObject["fats"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-fat"]')
    recipeObject["fats"] = recipeObject["fats"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["fats"] = re.sub("[^0-9]", "", recipeObject["fats"])

    # proteins
    recipeObject["proteins"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-protein"]')
    recipeObject["proteins"] = recipeObject["proteins"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["proteins"] = re.sub("[^0-9]", "", recipeObject["proteins"])

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]').text

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')

    for step in steps:
        recipeObject["steps"].append(step.text)

    for item in prep:
        recipeObject["prep"].append(item)

    return recipeObject

def cookingtree(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="attachment-penci-full-thumb size-penci-full-thumb wp-post-image"]').get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@class="post-title single-post-title entry-title"]').text)

    # time active
    recipeObject["timeActive"] = textTime( driver.find_element_by_xpath('//time[@itemprop="prepTime"]').text )

    # time waiting
    recipeObject["timeWaiting"] = textTime( driver.find_element_by_xpath('//time[@itemprop="totalTime"]').text )

    # serving amount
    recipeObject["servingsAmount"] = int( driver.find_element_by_xpath('//span[@class="servings"]').text )

    # servinging unit
    recipeObject["servingsUnit"] = 'Servings'

    # author
    recipeObject["author"] = 'The Cooking Tree'

    # ingredients
    ingredients = driver.find_elements_by_xpath('//li[@itemprop="recipeIngredient"]')

    for ingredient in ingredients:
        recipeObject["ingredients"].append(textToIngredient(ingredient.text))

    # calories

    # carbs

    # fats

    # proteins

    # description

    # steps
    steps = driver.find_element_by_xpath('//div[@class="penci-recipe-method"]')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # 

    return recipeObject

def skinnyTaste(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="lazyloaded"]').get_attribute('src')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.png', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h2[@class="wprm-recipe-name wprm-block-text-normal"]').text)

    # time active
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-table wprm-block-text-normal wprm-recipe-time-container wprm-recipe-prep-time-container"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])

    # time waiting
    recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-table wprm-block-text-normal wprm-recipe-time-container wprm-recipe-cook-time-container"]')
    recipeObject["timeWaiting"] = recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeWaiting"] = textTime(recipeObject["timeWaiting"])

    # serving amount
    try:
        recipeObject["servingsAmount"] = int(driver.find_element_by_xpath('//span[@class="wprm-recipe-servings wprm-recipe-details wprm-recipe-servings-49168 wprm-recipe-servings-adjustable-disabled wprm-block-text-normal"]').text)
    except:
        recipeObject["servingsAmount"] = 1

    # servings unit
    try:
        recipeObject["servingsUnit"] =titlecase( driver.find_element_by_xpath('//span[@class="wprm-recipe-servings-unit wprm-recipe-details-unit wprm-block-text-normal"]').text )
    except:
        recipeObject["servingsUnit"] = "Servings"

    # author
    recipeObject["author"] = "Gina Homolka of Skinny Taste"

    # ingredients
    ingredients = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')

    for ingredient in ingredients:
        ingredientWorking = [0.000, "", ""]

       # amount
        try:
            ingredientWorking[0] = ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text
        except:
            ingredientWorking[0] = 0.000

        # trying to make it float, assuming it is an easy conversion
        try:
            ingredientWorking[0] = float(ingredientWorking[0])
        except ValueError:
            # is the amount a frac char?
            try:
                ingredientWorking[0] = fracCharToFloat(ingredientWorking[0])
            except:
                # it is a string fractions
                ingredientWorking[0] = convertToFloat(ingredientWorking[0])
        except:
            ingredientWorking[0] = 0.000

        # unit
        try:
            ingredientWorking[1] = ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-unit"]').text

            if (str(ingredientWorking[1]).lower()) == 'g':
                ingredientWorking[1] = 'Grams'
            elif (str(ingredientWorking[1]).lower()) == 'ml':
                ingredientWorking[1] = 'Milliliters'
            elif (str(ingredientWorking[1]).lower()) == 'kg':
                ingredientWorking[1] = 'Kilograms'
            elif (str(ingredientWorking[1]).lower()) == 'tbs':
                ingredientWorking[1] = 'Tablespoon'
            elif (str(ingredientWorking[1]).lower()) == 'tbsp':
                ingredientWorking[1] = 'Tablespoon'
            elif (str(ingredientWorking[1]).lower()) == 'tsp':
                ingredientWorking[1] = 'Teaspoon'
            elif (str(ingredientWorking[1]).lower()) == 'lb':
                ingredientWorking[1] = 'Pounds'
            elif (str(ingredientWorking[1]).lower()) == 'oz':
                ingredientWorking[1] = 'Ounces'
        except:
            ingredientWorking[1] = 'Count'

        # name
        ingredientWorking[2] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-name"]').text)

        recipeObject["ingredients"].append(ingredientWorking)

    # calories
    try:
        recipeObject["calories"] = int( driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal"]').text )
    except:
        recipeObject["calories"] = 0

    # carbs
    try:
        recipeObject["carbs"] = int( driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-carbohydrates wprm-block-text-normal"]').text )
    except:
        recipeObject["carbs"] = 0

    # fats
    try:
        recipeObject["fats"] = int( driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-fat wprm-block-text-normal"]').text )
    except:
        recipeObject["fats"] = 0

    # proteins
    try:
        recipeObject["proteins"] = int( driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-protein wprm-block-text-normal"]').text )
    except:
        recipeObject["proteins"] = 0

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-italic"]').text

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

def vegRecipesOfIndia(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//div[@class="wp-block-image"]')
        image = image.find_element_by_tag_name('img').get_attribute('src')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        request_ = urllib.request.Request(image, None, headers)
        response = urllib.request.urlopen(request_)
        f = open('recipe.png', 'wb')
        f.write(response.read())
        f.close()
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h2[@class="wprm-recipe-name wprm-block-text-bold"]').text)

    # active time
    try:
        recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-bold wprm-recipe-time-container wprm-recipe-prep-time-container"]')
        recipeObject["timeActive"] = int(textTime(recipeObject["timeActive"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-bold"]').text))
    except:
        recipeObject["timeActive"] = 0

    # waiting time
    try:
        recipeObject["timeWaiting"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-bold wprm-recipe-time-container wprm-recipe-cook-time-container"]')
        recipeObject["timeWaiting"] = int((textTime(recipeObject["timeWaiting"].find_element_by_xpath('.//span[@class="wprm-recipe-time wprm-block-text-bold"]').text)))
    except:
        recipeObject["timeWaiting"] = 0

    # serving amount
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal wprm-recipe-servings-container"]')
    recipeObject["servingsAmount"] = int(recipeObject["servingsAmount"].find_element_by_tag_name('input').get_attribute('value'))

    # serving unit
    recipeObject["servingsUnit"] = "Servings"

    # author
    recipeObject["author"] = 'Dassana Amit of Vegetarian Recipes of India'

    # ingredients
    ingredients = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')

    for ingredient in ingredients:
        ingredientWorking = [0.000, "", ""]

        # amount
        try:
            ingredientWorking[0] = ingredient.find_element_by_class_name('wprm-recipe-ingredient-amount').text
        except:
            ingredientWorking[0] = 0.000

        # trying to make it float, assuming it is an easy conversion
        try:
            ingredientWorking[0] = float(ingredientWorking[0])
        except ValueError:
            # is the amount a frac char?
            try:
                ingredientWorking[0] = fracCharToFloat(ingredientWorking[0])
            except:
                # it is a string fractions
                try:
                    ingredientWorking[0] = convertToFloat(ingredientWorking[0])
                except:
                    ingredientWorking[0] = ingredient.text
                    ingredientWorking[0] = ingredientWorking[0].replace('▢ ', '')
                    ingredientWorking[0] = textToIngredient(ingredientWorking[0])[0]

        except:
            ingredientWorking[0] = 0.000

        # unit
        try:
            ingredientWorking[1] = titlecase(ingredient.find_element_by_class_name('wprm-recipe-ingredient-unit').text)
        except:
            ingredientWorking[1] = "Count"

        # name
        ingredientWorking[2] = titlecase(ingredient.find_element_by_class_name('wprm-recipe-ingredient-name').text)

        print(str(ingredientWorking))

        recipeObject["ingredients"].append(ingredientWorking)


    # calories
    recipeObject["calories"] =  driver.find_element_by_xpath('//div[@class="nutrition-item"]')
    recipeObject["calories"] = recipeObject["calories"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["calories"] = int(re.sub("[^0-9]", "", recipeObject["calories"]))

    # carbs
    recipeObject["carbs"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-carbohydrates"]')
    recipeObject["carbs"] = recipeObject["carbs"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["carbs"] = int(re.sub("[^0-9]", "", recipeObject["carbs"]))

    # fats
    recipeObject["fats"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-fat"]')
    recipeObject["fats"] = recipeObject["fats"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["fats"] = int(re.sub("[^0-9]", "", recipeObject["fats"]))

    # proteins
    recipeObject["proteins"] = driver.find_element_by_xpath('//div[@class="nutrition-item nutrition-item-protein"]')
    recipeObject["proteins"] = recipeObject["proteins"].find_element_by_xpath('.//span[@class="nutrition-main"]').text
    recipeObject["proteins"] = int(re.sub("[^0-9]", "", recipeObject["proteins"]))

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]').text

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags


    return recipeObject

def manjulasKitchen(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//a[@class="swipebox"]').get_attribute('href')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = driver.find_element_by_xpath('//header[@class="entry-header"]')
    recipeObject["title"] = titlecase(recipeObject["title"].find_element_by_tag_name('h1').text)

    # active time

    # waiting time

    # aerving amount
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]')
    recipeObject["servingsAmount"] = recipeObject["servingsAmount"].find_elements_by_xpath('span')[1].text
    recipeObject["servingsAmount"] = re.sub("[^0-9]", "", recipeObject["servingsAmount"])

    # serving unit
    recipeObject["servingsUnit"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]')
    recipeObject["servingsUnit"] = recipeObject["servingsUnit"].find_elements_by_xpath('span')[1].text
    recipeObject["servingsUnit"] = re.sub(r'[0-9]', '', recipeObject["servingsUnit"])

    # author
    recipeObject["author"] = "Manjula Jain of Manjula's Kitchen"

    # ingredients
    ingredients = driver.find_element_by_xpath('//div[@class="content-wrapper"]')
    ingredients = ingredients.find_element_by_tag_name('ul')
    ingredients = ingredients.find_elements_by_tag_name('li')

    for ingredient in ingredients:
        recipeObject["ingredients"].append(textToIngredient(ingredient.text))

    # calories

    # carbs

    # fats

    # proteins

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]')
    recipeObject["description"] = recipeObject["description"].find_elements_by_xpath('span')[0].text

    # steps
    steps = driver.find_element_by_xpath('//div[@class="wprm-recipe-instruction-group"]')
    steps = steps.find_element_by_tag_name('ul')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

def publix(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//img[@class="recipe-details-image"]')
        image = image.get_attribute('src')
        print(image)
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        try:
            image = driver.find_element_by_xpath('//img[@class="youtube-video-poster-image"]')
            image = image.get_attribute('src')
            print(image)
            urllib.request.urlretrieve(image, "recipe.png")
            recipeObject["image"] = True
        except:
            recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = driver.find_element_by_xpath('//h1[@class="recipe-details-name headline-small underline"]').text

    # active time

    # waiting time

    # serving amount
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//div[@class="recipe-details-servings"]').text

    recipeObject["servingsAmount"] = int(re.sub("[^0-9]", "", recipeObject["servingsAmount"]))

    # serving unit
    recipeObject["servingsUnit"] = driver.find_element_by_xpath('//div[@class="recipe-details-servings"]').text
    recipeObject["servingsUnit"] = titlecase(re.sub(r'[0-9]', '', recipeObject["servingsUnit"]))

    # author
    recipeObject["author"] = 'Publix Aprons'

    # ingredients
    ingredients = driver.find_element_by_xpath('//ul[@class="recipe-details-ingredients"]')
    ingredients = ingredients.find_elements_by_tag_name('li')
    prep = []

    for ingredient in ingredients:
        ingredientWorking = textToIngredient(ingredient.text)
        ingredientWorking, prep = ingredientFilter.main(ingredientWorking, prep)
        recipeObject["ingredients"].append(ingredientWorking)

    # calories
    nutrition = driver.find_element_by_xpath('//div[@class="accordion recipe-details-nutrition opened"]')
    nutrition = nutrition.find_element_by_xpath('.//div[@class="content"]').text.split('; ')
    print(nutrition)

    recipeObject["calories"] = nutrition[0].split()[4]

    print(recipeObject["calories"])

    recipeObject["calories"] = re.sub("[^0-9]", "", recipeObject["calories"])

    # carbs
    recipeObject["carbs"] = re.sub("[^0-9]", "", nutrition[6])

    # fats
    recipeObject["fats"] = re.sub(r'[^\d.]+', "", nutrition[1])

    # proteins
    recipeObject["proteins"] = re.sub(r'[^\d.]+', "", nutrition[9])

    # description

    # steps
    steps = driver.find_element_by_xpath('//ol[@class="recipe-details-instructions-list"]')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    #prep
    for item in prep:
        recipeObject["prep"].append(item)

    # tips

    # tags

    return recipeObject

def hotThaiKitchen(driver, recipeLink, recipeObject):

    # load
    driver.get(recipeLink)
    time.sleep(2)

    #image
    recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = driver.find_element_by_xpath('//h2[@class="tasty-recipes-title"]').text

    # active time

    # waiting time

    # serving amount

    # serving unit

    # author
    recipeObject["author"] = driver.find_element_by_xpath('//a[@class="tasty-recipes-author-name"]').text
    recipeObject["author"] = recipeObject["author"] + ' for Hot Thai Kitchen'

    # ingredients
    ingredients = driver.find_element_by_xpath('//div[@class="tasty-recipes-ingredients-body"]')
    ingredients = ingredients.find_elements_by_tag_name('li')

    for ingredient in ingredients:
        recipeObject["ingredients"].append(textToIngredient(ingredient.text))

    # calories

    # carbs

    # fats

    # proteins

    # description

    # steps
    steps = driver.find_element_by_xpath('//div[@class="tasty-recipes-instructions-body"]')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

def justOneCookbook(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//div[@class="entry-content "]')
        image = image.find_element_by_tag_name('img')
        image = image.get_attribute('src')
        #image = driver.find_element_by_xpath('//img[@class="aligncenter size-full lazyloaded"]').get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@class="entry-title"]').text)

    # time active
    recipeObject["timeActive"] = textTime(driver.find_elements_by_xpath('//span[@class="wprm-recipe-time wprm-block-text-normal"]')[0].text)
    '''
    recipeObject["timeActive"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-block-container wprm-recipe-block-container-table wprm-block-text-normal wprm-recipe-time-container wprm-recipe-prep-time-container"]')
    recipeObject["timeActive"] = recipeObject["timeActive"].find_element_by_xpath('//span[@class="wprm-recipe-time wprm-block-text-normal"]').text
    recipeObject["timeActive"] = textTime(recipeObject["timeActive"])
    '''
    # time waiting
    '''
    find element by 
    span class="wprm-recipe-time wprm-block-text-normal"
    index=1

    because the waiting time name can change
    '''
    recipeObject["timeWaiting"] = textTime(driver.find_elements_by_xpath('//span[@class="wprm-recipe-time wprm-block-text-normal"]')[1].text)

    # serving amount
    recipeObject["servingsAmount"] = int(driver.find_element_by_xpath('//span[@aria-label="Adjust recipe servings"]').text)

    # serving unit
    recipeObject["servingsUnit"] = 'Servings'

    # author
    recipeObject["author"] = driver.find_element_by_xpath('//span[@class="wprm-recipe-details wprm-recipe-author wprm-block-text-normal"]').text
    recipeObject["author"] += ' for Just One Cookbook'

    # ingredients
    ingredients = driver.find_elements_by_xpath('//li[@class="wprm-recipe-ingredient"]')

    # [amount, unit, name]
    for ingredient in ingredients:
        ingredientList = [0.000, "", ""]

        # amount
        try:
            ingredientList[0] = int(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text)
        except:

            try:
                ingredientList[0] = convertToFloat(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text)
            except:

                try:
                    ingredientList[0] = fracCharToFloat(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-amount"]').text)
                except:
                    ingredientList[0] = 0.000

        # unit
        try:
            # can find the unit
            ingredientList[1] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-unit"]').text)

            if ingredientList[1].lower() == 'tsp':
                ingredientList[1] = 'Teaspoon'
            elif ingredientList[1].lower() == 'tbsp':
                ingredientList[1] = 'Tablespoon'

        except:
            # cannot find unit
            ingredientList[1] = "Count"

        # name
        try:
            ingredientList[2] = titlecase(ingredient.find_element_by_xpath('.//span[@class="wprm-recipe-ingredient-name"]').text)
        except:
            pass

        recipeObject["ingredients"].append(ingredientList)


    # nutrition
    try:
        nutrition = driver.find_elements_by_xpath('//span[@class="wprm-nutrition-label-text-nutrition-container"]')

            # calories
        recipeObject["calories"] = int(nutrition[0].find_element_by_xpath('.//span[@class="wprm-nutrition-label-text-nutrition-value"]').text)

            # carbs
        recipeObject["carbs"] = int(nutrition[1].find_element_by_xpath('.//span[@class="wprm-nutrition-label-text-nutrition-value"]').text)

            # proteins
        recipeObject["proteins"] = int(nutrition[2].find_element_by_xpath('.//span[@class="wprm-nutrition-label-text-nutrition-value"]').text)

            # fats
        recipeObject["fats"] = int(nutrition[3].find_element_by_xpath('.//span[@class="wprm-nutrition-label-text-nutrition-value"]').text)

    except:
        pass

    # steps
    steps = driver.find_elements_by_xpath('//li[@class="wprm-recipe-instruction"]')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="wprm-recipe-summary wprm-block-text-normal"]').text

    return recipeObject

def newYorkTimeCooking(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # url
    recipeObject["url"] = recipeLink

    # image
    try:
        image = driver.find_element_by_xpath('//div[@class="media-container"]')
        image = image.find_element_by_tag_name('img')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@clas="recipe-title title name"]').text)

    # active time

    # waiting time

    # servings 
    recipeObject["servingsAmount"] = driver.find_element_by_xpath('//span[@class="recipe-yield-value"]').text
    recipeObject["servingsAmount"] = re.sub('[^0-9]','', recipeObject["servingsAmount"])

    # serving units
    recipeObject["servingsUnit"] = driver.find_element_by_xpath('//span[@class="recipe-yield-value"]').text
    recipeObject["servingsUnit"] = titlecase(re.sub(r'\d+', '', recipeObject["servingsUnit"]))

    # author
    recipeObject["author"] = driver.find_element_by_xpath('//div[@class="nytc---recipebyline---bylinePart"]')
    recipeObject["author"] = titlecase(recipeObject["author"].find_element_by_tag_name('a').text)

    # ingredients
    ingredients = driver.find_element_by_xpath('//ul[@class="recipe-ingredients"]')
    ingredients = ingredients.find_elements_by_tag_name('li')

    for ingredient in ingredients:
        recipeObject["ingredients"].append(textToIngredient(ingredient.text))

    # calories

    # carbs

    # fats

    # proteins

    # descriptions
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="topnote"]')
    recipeObject["description"] = recipeObject["description"].find_element_by_tag_name('p').text

    # steps
    steps = driver.find_element_by_xpath('//ol[@class="recipe-steps"]')
    steps = steps.find_elements_by_tag_name('li')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep

    # tips

    # tags

    return recipeObject

def fineCooking(driver, recipeLink, recipeObject):

    # load page
    driver.get(recipeLink)
    time.sleep(2)

    # image
    try:
        image = driver.find_element_by_xpath('//figure[@class="recipe__image--main"]')
        image = image.find_element_by_tag_name('img')
        image = image.get_attribute('src')
        urllib.request.urlretrieve(image, "recipe.png")
        recipeObject["image"] = True
    except:
        recipeObject["image"] = None

    # url
    recipeObject["url"] = recipeLink

    # title
    recipeObject["title"] = titlecase(driver.find_element_by_xpath('//h1[@class="recipe__title"]').text)

    # active time

    # waiting time

    # servings

    # servings unit

    # author
    recipeObject["author"] = driver.find_element_by_xpath('//span[@class="recipe__author"]')
    recipeObject["author"] = recipeObject["author"].find_element_by_tag_name('a').text

    # ingredients
    ingredients = driver.find_element_by_xpath('//div[@class="recipe__ingredients"]')

    #ingredients = ingredients.find_element_by_tag_name('ul')

    ingredients = ingredients.find_elements_by_tag_name('li')
    prep = []
    for ingredient in ingredients:
        print('ingredient test = "' + str(ingredient.text) + '"')
        if ingredient.text not in ["", None]:
            convertedIngredient = textToIngredient(ingredient.text)
            convertedIngredient, prep = ingredientFilter.main(convertedIngredient, prep)

            recipeObject["ingredients"].append(convertedIngredient)
           # recipeObject["ingredients"].append(textToIngredient(ingredient.text))
    

    try:

        # calories
        recipeObject["calories"] = driver.find_element_by_xpath('//div[@class="recipe__nutrition__details"]')
        recipeObject["calories"] = recipeObject["calories"].find_element_by_tag_name('li').get_attribute('innerHTML')
        recipeObject["calories"] = re.sub("[^0-9]", "", recipeObject["calories"])

        # carbs
        recipeObject["carbs"] = driver.find_element_by_xpath('//div[@class="recipe__nutrition__details"]')
        recipeObject["carbs"] = recipeObject["carbs"].find_elements_by_tag_name('li')[8].get_attribute('innerHTML')
        recipeObject["carbs"] = re.sub("[^0-9]", "", recipeObject["carbs"])

        # fats
        recipeObject["fats"] = driver.find_element_by_xpath('//div[@class="recipe__nutrition__details"]')
        recipeObject["fats"] = recipeObject["fats"].find_elements_by_tag_name('li')[2].get_attribute('innerHTML')
        recipeObject["fats"] = re.sub("[^0-9]", "", recipeObject["fats"])

        # proteins
        recipeObject["proteins"] = driver.find_element_by_xpath('//div[@class="recipe__nutrition__details"]')
        recipeObject["proteins"] = recipeObject["proteins"].find_elements_by_tag_name('li')[10].get_attribute('innerHTML')
        recipeObject["proteins"] = re.sub("[^0-9]", "", recipeObject["proteins"])
    except:
        pass

    # description
    recipeObject["description"] = driver.find_element_by_xpath('//div[@class="recipe__blurb"]').text

    # steps
    steps = driver.find_element_by_xpath('//div[@class="recipe__preparation"]')
    steps = steps.find_elements_by_tag_name('p')

    for step in steps:
        recipeObject["steps"].append(step.text)

    # prep
    for item in prep:
        recipeObject["prep"].append(item)

    # tip

    # tags

    return recipeObject

def main():

    driver = webdriver.Chrome(executable_path='./chromedriver.exe')

    # I want there to be two windows
    driverTandoori = webdriver.Firefox(executable_path='geckodriver.exe')

    print('\nReading recipes.txt...')
    # change to normal recipes and not random
    with open('recipes_random.txt', 'r') as recipes:
        recipes = recipes.read().splitlines()

    for recipeLink in recipes:
        print('_____________________________________________________\nOpening ' + recipeLink)

        recipeObject = {
            "url": "",
            "title": "",
            "timeActive": 0,
            "timeWaiting": 0,
            "servingsAmount": 0,
            "servingsUnit": "",
            "author": "",
            "ingredients": [],
            "calories": 0,
            "carbs": 0,
            "fats": 0,
            "proteins": 0,
            "description": "",
            "steps": [],
            "prep": [],
            "tips": [],
            "tags": []
        }

        if 'altonbrown.com' in recipeLink:
            recipeObject = altonBrown(driver, recipeLink, recipeObject)
        elif 'bonappetit.com' in recipeLink:
            recipeObject = bonappetit(driver, recipeLink, recipeObject)
        elif 'simplyrecipes.com' in recipeLink:
            recipeObject = simplyrecipes(driver, recipeLink, recipeObject)
        elif 'epicurious.com' in recipeLink:
            recipeObject = epicurious(driver, recipeLink, recipeObject)
        elif 'sbs.com.au' in recipeLink:
            recipeObject = sbs(driver, recipeLink, recipeObject)
        elif 'thewoksoflife.com' in recipeLink:
            recipeObject = woksOfLife(driver, recipeLink, recipeObject)
        elif 'seriouseats.com' in recipeLink:
            recipeObject = seriousEats(driver, recipeLink, recipeObject)
        elif 'finecooking.com' in recipeLink:
            recipeObject = fineCooking(driver, recipeLink, recipeObject)
        elif 'food52.com' in recipeLink:
            recipeObject = food52(driver, recipeLink, recipeObject)
        elif 'cooking.nytimes.com' in recipeLink:
            pass
            #recipeObject = newYorkTimeCooking(driver, recipeLink, recipeObject)
        elif 'justonecookbook.com' in recipeLink:
            recipeObject = justOneCookbook(driver, recipeLink, recipeObject)
        elif 'hot-thai-kitchen.com' in recipeLink:
            recipeObject = hotThaiKitchen(driver, recipeLink, recipeObject)
        elif 'publix.com' in recipeLink:
            recipeObject = publix(driver, recipeLink, recipeObject)
        elif 'manjulaskitchen.com' in recipeLink:
            recipeObject = manjulasKitchen(driver, recipeLink, recipeObject)
        elif 'vegrecipesofindia.com' in recipeLink:
            recipeObject = vegRecipesOfIndia(driver, recipeLink, recipeObject)
        elif 'skinnytaste.com' in recipeLink:
            recipeObject = skinnyTaste(driver, recipeLink, recipeObject)
        elif 'en.cooking-tree.com' in recipeLink:
            recipeObject = cookingtree(driver, recipeLink, recipeObject)
        elif 'veganricha.com' in recipeLink:
            recipeObject = veganRicha(driver, recipeLink, recipeObject)
        elif 'budgetbytes.com' in recipeLink:
            recipeObject = budgetBytes(driver, recipeLink, recipeObject)
        '''
        print(
            '\nURL: '           + str(recipeObject["url"]) + 
            '\nTitle: '         + str(recipeObject["title"]) + 
            '\nActive Time: '   + str(recipeObject["timeActive"]) + 
            '\nWaiting Time: '  + str(recipeObject["timeWaiting"]) + 
            '\nServings: '      + str(recipeObject["servingsAmount"]) + ' ' + recipeObject["servingsUnit"] + 
            '\nAuthor: '        + recipeObject["author"] + 
            '\nIngredients: '   + str(recipeObject["ingredients"]) + 
            '\nCalories: '      + str(recipeObject["calories"]) + 
            '\nCarbs: '         + str(recipeObject["carbs"]) +
            '\nFats: '          + str(recipeObject["fats"]) + 
            '\nProteins: '      + str(recipeObject["proteins"]) + 
            '\nDescription: '   + recipeObject["description"] + 
            '\nSteps: '         + str(recipeObject["steps"]) + 
            '\nPrep: '          + str(recipeObject["prep"]) + 
            '\nTips: '          + str(recipeObject["tips"]) + 
            '\nTags: '          + str(recipeObject["tags"])
        )
        '''

        addToTandoori(driverTandoori, recipeObject)

        #print('Save or delete shown recipe?')
        saveRecipe = query_yes_no('Save (y) or delete (n) shown recipe?')

        if saveRecipe:
            button = driverTandoori.find_element_by_xpath('//button[@title="Ctrl + S"]').click()
        else:
            button = driverTandoori.find_element_by_xpath('//a[contains(@class, "btn-danger")]').click()
            button = driverTandoori.find_element_by_xpath('//button[@type="submit"]').click()

        recipeObject = None
        del recipeObject
        print('loading next page(s)')
        time.sleep(5)

        #time.sleep(9999999999999)
            
            
        
        
        

    
if __name__:
    main()