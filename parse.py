import bs4
import json
from collections import defaultdict
def remove_badges(soup, label):
    badges = soup.find_all(class_=label)
    for badge in badges:
        badge.decompose()

def deconstruct_tier(tier_soup):
    rows = tier_soup.find_all('tr')
    headers = [column.text for column in rows.pop(0).find_all('th')]
    tiers = [{name : column.text 
        for name, column in zip(headers, row.find_all('td'))}
        for row in rows]
    return tiers

def parse_mod(table):
    mod_tiers = defaultdict(list)
    categories = table.find_all('div', {'class': 'mod-title'})
    tiers = table.find_all('div', {'class': 'modal fade'})
    for category, tier in zip(categories, tiers):
        remove_badges(category, 'label')
        remove_badges(category, 'badge')
        tier_dict = deconstruct_tier(tier)
        category = category.text.strip()
        if '+' not in category[2:]:
            mod_tiers[category] += [tier_dict]
        else:    
            category1, category2 = category.rsplit('+', 1)
            category2 = '+' + category2
            mod_tiers[category1] += [tier_dict]
            mod_tiers[category2] += [tier_dict]

    return mod_tiers

names = ['ring', 'amulet', 'sceptre', 'wand', 'boots', 'gloves', 'helmet', 'shield']
for name in names:
    with open(f'data/synth_{name}.json') as fp:
        synth = json.load(fp)
    # actual html need to fix this later
    with open(f'data/prefix_{name}.json') as fp:
        website = fp.read()

    soup = bs4.BeautifulSoup(website, 'lxml')
    prefixes = soup.find_all('div', {'class': 'col-lg-6 float-left'})
    suffixes = soup.find_all('div', {'class': 'col-lg-6 float-right'})
   
    main_prefix = prefixes[0]
    
    mod_synths = defaultdict(list)
    for mod in synth['data']:
        soup = [bs4.BeautifulSoup(submod, 'lxml') for submod in mod]
        category, values, mods = soup
        lower, upper = values.text.split('~')
        if not lower.strip():
            lower = 0
        lower, upper = int(lower), int(upper)
        mods = [mod.text for mod in mods.find_all('li')] or mods.text
        mod_synths[category.text] += [(lower, mods)]

    mod_synth = {category : sorted(mods)[-1] for category, mods in mod_synths.items()}

    with open(f'data/parsed_{name}.json', 'w') as fp:
        json.dump({
            'prefixes': parse_mod(prefixes[0]),
            'suffixes': parse_mod(suffixes[0]),
            'synth':mod_synth,
            }, 
        fp)

        
