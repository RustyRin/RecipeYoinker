'''
This is my first attempt at
category scraping

the idea is that the bot will go
though a list of links to the
categories the site and then go
to each page of that category
then go on to the next category
'''

import requests
from bs4 import BeautifulSoup
from urllib import *
import time


categories = [
    'https://cooking.nytimes.com/68861692-nyt-cooking/103-centerpiece-desserts',
    'https://cooking.nytimes.com/68861692-nyt-cooking/465-cooking-with-julia-child',
    "https://cooking.nytimes.com/68861692-nyt-cooking/477-our-favorite-granolas",
    'https://cooking.nytimes.com/68861692-nyt-cooking/16596-healthy-breakfasts-that-happen-to-be-delicious',
    'https://cooking.nytimes.com/68861692-nyt-cooking/484-kid-friendly-cooking',
    'https://cooking.nytimes.com/68861692-nyt-cooking/16707-veggie-burgers',
    'https://cooking.nytimes.com/68861692-nyt-cooking/18801-french-at-home',
    'https://cooking.nytimes.com/68861692-nyt-cooking/36033-15-great-green-bean-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/26963-53-weekend-breakfast-ideas',
    'https://cooking.nytimes.com/68861692-nyt-cooking/26963-53-weekend-breakfast-ideas',
    'https://cooking.nytimes.com/68861692-nyt-cooking/54961-great-rice-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/90084-zucchini-for-breakfast-lunch-and-dinner',
    'https://cooking.nytimes.com/68861692-nyt-cooking/382788-25-great-pancake-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/369703-things-you-should-make-not-buy',
    'https://cooking.nytimes.com/68861692-nyt-cooking/408832-our-100-best-chocolate-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/475694-easy-weeknight-noodles',
    'https://cooking.nytimes.com/68861692-nyt-cooking/638891-113-warming-stews-and-soups',
    'https://cooking.nytimes.com/68861692-nyt-cooking/562858-so-many-smoothies-so-little-time',
    'https://cooking.nytimes.com/68861692-nyt-cooking/786277-quick-bread-recipes-for-the-carb-hungry-and-time-starved',
    'https://cooking.nytimes.com/68861692-nyt-cooking/786444-comforting-pudding-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/839100-valentines-day-dinner-ideas-and-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/807889-20-great-chili-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/873428-casseroles-for-cold-nights',
    'https://cooking.nytimes.com/68861692-nyt-cooking/884094-cookie-recipes-to-satisfy-your-sweet-tooth',
    'https://cooking.nytimes.com/68861692-nyt-cooking/907513-potatoes-beyond-baked',
    'https://cooking.nytimes.com/68861692-nyt-cooking/886707-6-of-melissa-clarks-best-weeknight-dinners',
    'https://cooking.nytimes.com/68861692-nyt-cooking/910360-best-dip-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/953691-26-meatless-mushroom-recipes-from-martha-rose-shulman',
    'https://cooking.nytimes.com/68861692-nyt-cooking/970976-vegetarian-comfort-food',
    'https://cooking.nytimes.com/68861692-nyt-cooking/961504-amazing-ways-to-do-macaroni-and-cheese',
    'https://cooking.nytimes.com/68861692-nyt-cooking/996375-lovely-layer-cakes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/999915-26-amazing-asparagus-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1024147-a-quiche-for-every-occasion',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1001747-the-greatest-lasagna-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1034957-broccoli-doesnt-have-to-be-boring',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1034971-carrot-side-dishes-that-deserve-a-starring-role',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1036964-sunday-supper-roast-chicken',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1045989-muffins-scones-and-biscuits-oh-my',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1054385-22-delicious-reasons-to-eat-cake-for-breakfast',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1053870-everyone-loves-pie-61-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1073191-the-vegetarian-sandwich',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1092797-classic-sandwiches',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1176003-italian-cocktails',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1128349-fried-rice-heaven',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1176016-swedish-dishes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1218861-vegetarian-grilling-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1284196-no-bake-desserts-for-lazy-days',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1237735-grilling-bbq-side-dishes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1284303-casseroles-for-brunch',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1334836-easy-weeknight-salmon',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1604305-easy-weeknight-dinners',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1415105-let-them-eat-brownies',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1415105-let-them-eat-brownies',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1661598-mark-bittmans-most-popular-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1661737-sam-siftons-most-popular-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1663983-melissa-clarks-most-popular-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1666633-our-most-popular-pork-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1689597-our-ultimate-mashed-potato-recipe-collection',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1685632-34-desserts-for-apple-season',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1689996-our-most-popular-vegetarian-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1734674-classic-italian-sauces-you-should-know-by-heart',
    'https://cooking.nytimes.com/68861692-nyt-cooking/1834106-mark-bittman-dessert-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2112870-scrambled-egg-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2274598-easy-30-minute-vegetarian-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2274410-want-a-frittata',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2280873-classic-dishes-you-should-perfect-if-you-havent-already',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2301017-24-classic-chicken-dishes-you-should-know',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2364067-18-kid-friendly-dishes-that-can-really-be-ready-in-30-minutes'
    'https://cooking.nytimes.com/68861692-nyt-cooking/2370458-because-the-dishwasher-is-you-delicious-one-pot-or-pan-dinners',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2435006-16-of-our-favorite-sides-for-roast-chicken',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2405852-a-sunday-kind-of-roast',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2437023-7-iconic-times-dishes-you-should-add-to-your-repertoire',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2504200-bean-dips-and-spreads',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2535930-16-of-our-most-popular-lemon-desserts',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2556504-bean-and-lentil-burgers',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2556520-lentil-soups-dals-and-stews',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2566152-easy-fish-recipes-that-arent-salmon',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2556520-lentil-soups-dals-and-stews',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2566152-easy-fish-recipes-that-arent-salmon',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2579391-practically-magical-3-ingredient-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2583132-26-delicious-dinners-in-5-ingredients-or-fewer',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2625403-almost-as-good-as-a-full-nights-sleep-29-dishes-to-cook-for-new-parents',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2662470-31-ways-to-eat-eggs-for-dinner',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2662871-what-to-cook-when-youd-rather-be-doing-anything-else',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2668820-easy-recipes-that-make-you-look-like-a-better-cook-than-you-are',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2692288-got-a-can-of-chickpeas-dinners-almost-done',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2715073-our-favorite-weeknight-pastas-from-mark-bittman',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2733298-staff-favorite-side-dishes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2780462-19-vegetarian-ish-weeknight-pasta-dishes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/2825551-crazy-fast-dinners-ready-in-20-minutes-or-less',
    'https://cooking.nytimes.com/68861692-nyt-cooking/29440-burger-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3278066-dishes-that-taste-better-on-the-second-or-third-day',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3360366-easy-and-cheap-pastas-most-of-them-vegetarian',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3360788-26-classic-comfort-food-dinners',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3370866-25-of-our-most-popular-potato-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3446155-easy-recipes-that-will-impress-your-family-and-friends',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3450320-our-20-most-popular-cauliflower-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3543047-easy-weeknight-soups',
    'https://cooking.nytimes.com/68861692-nyt-cooking/3586435-election-day-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4229631-cheap-eats-for-those-of-us-on-a-budget',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4448474-16-marvelous-rubs-and-marinades-you-should-save',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4470440-10-of-our-most-popular-dips',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4506968-14-one-hour-or-less-chocolate-desserts-and-treats',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4844254-vegetarian-dishes-to-bring-to-a-potluck',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4862456-13-tomato-soups-that-are-great-with-or-without-grilled-cheese',
    'https://cooking.nytimes.com/68861692-nyt-cooking/4915281-21-of-our-most-popular-vegetarian-soups',
    'https://cooking.nytimes.com/68861692-nyt-cooking/6980515-our-10-most-popular-zucchini-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/7543357-fast-dinners-for-hungry-busy-people',
    'https://cooking.nytimes.com/68861692-nyt-cooking/7796440-sausage-the-weeknight-cooks-saving-grace',
    'https://cooking.nytimes.com/68861692-nyt-cooking/7897491-vegetarian-comfort-food-in-an-hour-or-less',
    'https://cooking.nytimes.com/68861692-nyt-cooking/8897128-13-dessert-bars-you-can-eat-with-one-hand',
    'https://cooking.nytimes.com/68861692-nyt-cooking/9552706-a-side-of-rice',
    'https://cooking.nytimes.com/68861692-nyt-cooking/9787590-our-10-most-popular-chicken-recipes-right-now',
    'https://cooking.nytimes.com/68861692-nyt-cooking/10124841-our-15-most-popular-breakfast-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/10278553-our-20-most-popular-pasta-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/10459814-our-20-most-popular-salmon-recipes',
    'https://cooking.nytimes.com/68861692-nyt-cooking/101-times-classics'
]

def main(fullPath):
    #siteName        = 'https://www.vegrecipesofindia.com/recipes/?fwp_paged=1'
    className       = "card-recipe-info"
    cacheName       = str(fullPath) + '/sites/nytcooking/nytcooking.txt'
    recipesOnPage   = True

    for siteName in categories:
        print('\n\n\nWORKING ON CATEGORY ' + siteName)
        recipesOnPage = True
        while recipesOnPage is True:
            soup = BeautifulSoup(requests.get(siteName).content, 'html.parser')
            time.sleep(5)

            # finding all recipes on page
            recipesOnPage = False
            for i in soup.find_all(class_=className):
                recipeLink = i['href']
                recipesOnPage = True
                # Read all cached links
                with open(cacheName, 'r') as cache:
                    existing = cache.read().splitlines()

                if recipeLink not in existing:
                    print("Adding " + recipeLink)

                    with open(cacheName, 'a+') as cache:
                        existing.append(recipeLink)
                        cache.write(recipeLink + '\n')

                    if ('https://cooking.nytimes.com' not in recipeLink):
                        recipeLink = 'https://cooking.nytimes.com' + recipeLink

                    with open(str(fullPath) + '/recipes.txt', 'a+') as recipes:
                        recipes.write(recipeLink + '\n')
                else:
                    print('Alread have ' + recipeLink)
                recipesOnPage = False
                
            if recipesOnPage is False:
                print('NO RECIPES FOUND ON PAGE, SCRAPE DONE')
                recipesOnPage = False
            
