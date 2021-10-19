with open('recipes.txt', 'r') as f:
    unique_lines = set(f.readlines())

with open('recipes_no_dupes.txt', 'w') as f:
    f.writelines(unique_lines)