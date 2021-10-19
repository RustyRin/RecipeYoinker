'''
This removes things prep work
from the ingredient names and
moves them to the prep array
'''

from titlecase import titlecase
import re

def main(ingredient, prep):

    print('old ingredient: ' + str(ingredient))

    # if prep no exist, start it
    if prep is None:
        prep = []

    # teaspoon
    if 'tsp.' in ingredient[2].lower():
        ingredient[1] = 'Teaspoon'
        ingredient[2] = titlecase(ingredient[2].replace('tsp. ', ''))

    # tablespoon
    if 'tbsp.' in ingredient[2].lower():
        ingredient[1] = 'Tablespoon'
        ingredient[2] = titlecase(ingredient[2].replace('Tbsp. ', ''))

    if ('cup' in ingredient[2].lower()) and ('plus' not in ingredient[2].lower()):
        ingredient[1] = 'Cup'
        ingredient[2] = titlecase(ingredient[2].replace('cup ', ''))

    if 'oz' in ingredient[2].lower():
        if 'oz.' in ingredient[2].lower():
            ingredient[1] = 'Ounces'
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace('oz. ', ''))
        else:
            ingredient[1] = 'Ounces'
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace('oz ', ''))

    # removing seeds should be first,
    # you dont want the prep to read
    # "dice, then remove seeds"
    if 'seed' in ingredient[2].lower():
        if ', seeded for less heat if desired' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', seeded for less heat if desired', ''))
            
            prep.append('- If you want the dish to be less hot, remove the seeds from the ' + ingredient[2])
        if ', seeds removed' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', seeds removed', ''))
            
            prep.append('- Remove the seeds from the ' + ingredient[2])


    # peeled
    if 'peel' in ingredient[2].lower() and 'unpeeled' not in ingredient[2].lower():

            if ', peeled' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace(', peeled', '')
                ingredient[2] = titlecase(ingredient[2])

                prep.append('- Peel the ' + ingredient[2])
            elif 'peeled' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace('peeled', '')
                ingredient[2] = titlecase(ingredient[2])

                prep.append('- Peel the ' + ingredient[2])
            elif 'peel' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace('peel', '')
                ingredient[2] = titlecase(ingredient[2])

                prep.append('- Peel the ' + ingredient[2])

    # chopped
    if 'chopped' in ingredient[2].lower():
        if ", chopped" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', chopped', ''))

            prep.append('- Chop the ' + ingredient[2])

        elif ', coarsely chopped' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', coarsely chopped', ''))

            prep.append('- Coarsely chop the ' + ingredient[2])

        elif ', roughly chopped' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', roughly chopped', ''))

            prep.append('- Roughly chop the ' + ingredient[2])

        elif ', finely chopped 'in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', finely chopped ', ''))

            prep.append('- Finely chop the ' + ingredient[2])
        elif ', finely chopped' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', finely chopped', ''))

            prep.append('- Finely chop the ' + ingredient[2])
        
        elif 'finely chopped' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace('finely chopped', ''))

            prep.append('- Finely chop the ' + ingredient[2])
        elif 'chopped fine' in ingredient[2].lower():
            if ', chopped fine' in ingredient[2].lower():
                ingredient[2] = titlecase(ingredient[2].replace(', chopped fine', ''))
            else:
                ingredient[2] = titlecase(ingredient[2].replace('chopped fine', ''))
            ingredient[2] = ingredient[2].lower()

            prep.append('- Finely chop the ' + ingredient[2])
        elif 'chopped 'in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace('chopped', ''))

            prep.append('- Chop the ' + ingredient[2])

    # cut thing
    if 'cut' in ingredient[2].lower():

        # into 1/2 inch cubes
        if ", cut into 1/2-inch cubes" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', cut into 1/2-inch cubes', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into 1/2 inch cubes')

        elif 'cut into 1-inch cubes' in ingredient[2].lower():
            if ", cut into 1-inch cubes" in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = titlecase(ingredient[2].replace(', cut into 1-inch cubes', ''))
                
                prep.append('- Cut the ' + ingredient[2] + ' into 1 inch cubes')
            else:
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = titlecase(ingredient[2].replace('cut into 1-inch cubes', ''))
                
                prep.append('- Cut the ' + ingredient[2] + ' into 1 inch cubes')

        elif ", cut into large chunks" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', cut into large chunks', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into large chunks')

        # into 3-inch lengths
        elif ", cut into 3-inch lengths" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', cut into 3-inch lengths', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into 3 inch lengths')

        elif ", cut into 1/2-inch pieces" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', cut into 1/2-inch pieces', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into 1/2 inch pieces')
        elif ", cut into 1-inch pieces" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', cut into 1-inch pieces', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into 1 inch pieces')

    # cut thing in half
    if ', halved' in ingredient[2].lower():
        ingredient[2] = ingredient[2].lower()
        ingredient[2] = titlecase(ingredient[2].replace(', halved', ''))
        
        prep.append('- Cut ' + ingredient[2] + ' in half')

    if 'sliced' in ingredient[2].lower():
        if ", sliced thinly on the bias" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', sliced thinly on the bias', ''))
            
            prep.append('- Slice the ' + ingredient[2] + ' thinly on the bias')
        elif 'thinly sliced' in ingredient[2].lower():
            if ', thinly sliced' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = titlecase(ingredient[2].replace(', thinly sliced', ''))
            else:
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = titlecase(ingredient[2].replace('thinly sliced', ''))
            
            prep.append('- Thinly slice the ' + ingredient[2])

    if 'quartered' in ingredient[2].lower():
         if ", quartered" in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', quartered', ''))
            
            prep.append('- Cut the ' + ingredient[2] + ' into quarters')


    if 'dice' in ingredient[2].lower():

        if ', diced into 1/2-inch cubes' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', diced into 1/2-inch cubes', ''))
            
            prep.append('- Dice the ' + ingredient[2] + ' into 1/2 inch cubes')
        elif 'diced' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', diced', ''))
            
            prep.append('- Dice the ' + ingredient[2])

    if ', scrubbed and rinsed' in ingredient[2].lower():
        ingredient[2] = ingredient[2].lower()
        ingredient[2] = titlecase(ingredient[2].replace(', scrubbed and rinsed', ''))
            
        prep.append('- Scrub and rinse the ' + ingredient[2])

    # remove the more for sprinkling
    if ', plus more for sprinkling' in ingredient[2].lower():
        ingredient[2] = titlecase(ingredient[2].replace(', plus more for sprinkling', ''))

    if ', warmed' in ingredient[2].lower():
        if ', warmed (for serving)' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', warmed (for serving)', ''))
                
            prep.append('- When serving, warm the ' + ingredient[2])

    if 'divided' in ingredient[2].lower():
        if ', divided' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', divided', '')
            ingredient[2] = titlecase(ingredient[2])
    
    if 'split lengthwise' in ingredient[2].lower():

        if ', split lengthwise' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = titlecase(ingredient[2].replace(', split lengthwise', ''))
        
            prep.append('- Split the ' + ingredient[2] + ' lengthwise')


    if 'minced' in ingredient[2].lower():

        if 'finley' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace('finely minced', '')
            ingredient[2] = titlecase(ingredient[2])
            prep.append('- Finley mince the ' + ingredient[2])

        else:
            if ', minced' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace(', minced', '')
                ingredient[2] = titlecase(ingredient[2])
                prep.append('- Mince the ' + ingredient[2])
            elif 'minced ' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace('minced ', '')
                ingredient[2] = titlecase(ingredient[2])
                prep.append('- Mince the ' + ingredient[2])
        


    if 'crumbled' in ingredient[2].lower():
            if ', crumbled' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace(', crumbled', '')
                ingredient[2] = titlecase(ingredient[2])

                prep.append('- Crumble the ' + ingredient[2])
            elif 'crumbled' in ingredient[2].lower():
                ingredient[2] = ingredient[2].lower()
                ingredient[2] = ingredient[2].replace('crumbled', '')
                ingredient[2] = titlecase(ingredient[2])

                prep.append('- Crumble the ' + ingredient[2])

    if 'trimmed' in ingredient[2].lower():

        if ', trimmed' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', trimmed', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Trim the ' + ingredient[2])

    if 'grated' in ingredient[2].lower():

        if ', grated on a microplane grater' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', grated on a microplane grater', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Grate the ' + ingredient[2] + ' on a microplane grater')

    if 'drained' in ingredient[2].lower():
        ingredient[2] = ingredient[2].lower()
        ingredient[2] = ingredient[2].replace('drained', '')
        ingredient[2] = titlecase(ingredient[2])

        prep.append('- Drain the ' + ingredient[2])

    if 'dry' in ingredient[2].lower():

        if 'patted dry on paper towels' in ingredient[2].lower():

            ingredient[2] = ingredient[2].replace('patted dry on paper towels', '')

            if 'and' in ingredient[2].lower():
                ingredient[2] = ingredient[2].replace('and', '')

            if ',' in ingredient[2].lower():
                ingredient[2] = ingredient[2].replace(',', '')
            
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Pat the ' + ingredient[2] + ' dry on some paper towels')
            
    if 'cored' in ingredient[2].lower():

        if ', cored' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', cored', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Core the ' + ingredient[2])

    if 'husks and stems removed' in ingredient[2].lower():
        if ', husks and stems removed' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', husks and stems removed', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Remove the husks and stems from the ' + ingredient[2])

    if 'rinsed' in ingredient[2].lower():
        if ', rinsed' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', rinsed', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Rinse the ' + ingredient[2])

    if 'toasted lightly' in ingredient[2].lower():
        if ', toasted lightly' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', toasted lightly', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Lightly toast the ' + ingredient[2])

    if 'grated' in ingredient[2].lower():
        if ', coarsely grated' in ingredient[2].lower():
            ingredient[2] = ingredient[2].lower()
            ingredient[2] = ingredient[2].replace(', coarsely grated', '')
            ingredient[2] = titlecase(ingredient[2])

            prep.append('- Coarsely grate the ' + ingredient[2])

    # finished

    # removing redundant spaces
    ingredient[2] = re.sub(' +', ' ', ingredient[2])    # remove double spaces
    ingredient[2] = ingredient[2].lstrip(' ')
    print('new ingredient: ' + str(ingredient))
    return (ingredient, prep)
