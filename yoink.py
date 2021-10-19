'''
This file opens various websites and then
tries to get as many new recipe links it
can see. 

It checks if its seen this link/recipe
before (from the individual site cache)
If it has seen the recipe before then it
skips it.

It then pastes/appends the links to the
recipes.txt file
'''

import pathlib

'''
Site imports
'''
from sites.vegrecipesofindia import vegrecipesofindia
from sites.sbs import sbs
from sites.atk import atk
from sites.skinnytaste import skinnytaste
from sites.manjulaskitchen import manjulaskitchen
from sites.finecooking import finecooking
from sites.epicurious import epicurious
from sites.bonappetit import bonappetit
from sites.food52 import food52
from sites.publixaprons import publixaprons
from sites.seriouseats import seriouseats
from sites.simplyrecipes import simplyrecipes
from sites.hotthaikitchen import hotthaikitchen
from sites.budgetbytes import budgetbytes
from sites.veganricha import veganricha
from sites.justonecookbook import justonecookbook
from sites.maangchi import maangchi
from sites.nytcooking import nytcooking
from sites.altonbrown import altonbrown
from sites.kaf import kaf
from sites.woksOfLife import woksOfLife
from sites.cookingTree import cookingTree

import random

'''
Sites to scrape
'''

sites = ['https://www.vegrecipesofindia.com/recipes/?fwp_paged=20']

for site in sites:


    # getting the full path to hand to 
    # each sites module to find their cache files
    fullPath = pathlib.Path('recipes.txt').parent.resolve()

    #altonbrown.main(fullPath)
    #justonecookbook.main(fullPath)
    veganricha.main(fullPath)
    #budgetbytes.main(fullPath)
    #hotthaikitchen.main(fullPath)
    #simplyrecipes.main(fullPath)
    #seriouseats.main(fullPath)
    #food52.main(fullPath)
    #epicurious.main(fullPath)
    #skinnytaste.main(fullPath)
    #finecooking.main(fullPath)     # does not stop
    #manjulaskitchen.main(fullPath)
    #sbs.main(fullPath)
    #vegrecipesofindia.main(fullPath)
    #publixaprons.main(fullPath)     # needs a way to gracfully fail when loadmore isnt there
    #bonappetit.main(fullPath)
    #woksOfLife.main(fullPath)
    #cookingTree.main(fullPath)

    '''
    lines_seen = set() # holds lines already seen
    outfile = open('./recipes_no_dupes.txt', "w")
    for line in open('./recipes.txt', "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    '''
    with open('./recipes.txt','r') as source:
        data = [ (random.random(), line) for line in source ]
    data.sort()
    with open('./recipes_random.txt','w') as target:
        for _, line in data:
            target.write( line )



