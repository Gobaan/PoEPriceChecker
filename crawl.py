import requests

session = requests.Session()
types = ['Ring', 'Amulet', 'Sceptre', 'Wand', 'Boots&an=dex_armour', 'Gloves&an=dex_armour', 'Helmet&an=dex_armour', 'Shield&an=int_armour,focus']
for type in types[-1:]:
    synth_link = f'https://poedb.tw/us/json.php/Synthesis/ItemSynthesisModsByItemClasses?cn={type}'
    prefix_link = f'https://poedb.tw/us/mod.php?cn={type}'
    print (prefix_link) 
    name = type[:type.index('&')] if '&' in type else type
    name = name.lower()
    response = session.get(synth_link)
    with open(f'data/synth_{name}.json', 'w') as fp:
        fp.write(response.text)
    response = session.get(prefix_link)
    with open(f'data/prefix_{name}.json', 'w') as fp:
        fp.write(response.text)
