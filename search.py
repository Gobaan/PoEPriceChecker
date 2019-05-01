import requests
import json

LEAGUE_MAPPER = {
  'Softcore Current': 0,
  'Hardcore Current': 1,
  'Softcore': 2,
  'Hardcore': 3,
}

# process to get filters:
# open http://www.pathofexile.com/trade/search/Synthesis/10w8Sg
# look at network traffic for trade.{uniqd.js
# search for weapon.one, that codeblock should have the filters in a fancy format
# format into something useful
FILTER_LIST = {
  "type_filters":  {
    "category" : [
       "weapon.bow",
       "weapon.claw",
       "weapon.dagger",
       "weapon.oneaxe",
       "weapon.onemace",
       "weapon.onesword",
       "weapon.sceptre",
       "weapon.staff",
       "weapon.twoaxe",
       "weapon.twomace",
       "weapon.twosword",
       "weapon.wand",
       "armour.chest",
       "armour.boots",
       "armour.gloves",
       "armour.helmet",
       "armour.shield",
       "armour.quiver",
       "accessory.amulet",
       "accessory.belt",
       "accessory.ring",
    ],
    "rarity" : ['nonunique'],
  }
}

session = requests.Session()

class Filter(object):
    # maytbe make this object print a list of options
    def __init__(self, category='weapon.twoaxe', rarity='nonunique', implicits=[], explicits=[], fractured=[]):
      self.filter_data = {
            "query": {
                "status": {
                    "option": "online"
                },
                "stats": [{
                    "type": "and",
                    "filters": implicits + explicits + fractured
                }],
                "filters": {
                    "type_filters": {
                        "filters": {
                            "category": {
                                "option": category
                            },
                            "rarity": {
                                "option": rarity,
                            }
                        }
                    }
                }
            },
            "sort": {
                "price": "asc"
            }
        }

def search(stash_api, custom_filter):
    response = session.post(stash_api, json=custom_filter.filter_data)
    results = json.loads(response.text)
    query = results['id']

    if not results['result']:
        return []
    result = ','.join(results['result'][:10])
    result_api = f'https://www.pathofexile.com/api/trade/fetch/{result}?query={query}'  
    print (result_api)
    response = session.get(result_api)
    return json.loads(response.text)

def full_search():

    response = session.get('https://www.pathofexile.com/api/trade/data/leagues')
    league = json.loads(response.text)
    league = league['result'][LEAGUE_MAPPER['Softcore Current']]['id']
    stash_api = f'https://www.pathofexile.com/api/trade/search/{league}'
    response = session.get('https://www.pathofexile.com/api/trade/data/stats')
    stats = json.loads(response.text)
    label_name_statid = { result['label'] : 
            {entry['text']: entry['id'] for entry in result['entries']}
            for result in stats['result'] }
    print (label_name_statid['Fractured'])
    print (label_name_statid['Implicit'])

    for category in FILTER_LIST["type_filters"]["category"]:
        custom_filter = Filter(category=category)
        #print(search(stash_api, custom_filter))

# Cross reference synthesis implicit mods with items they appear on
# TODO: loop over implicits to determine their value
# TODO: loop over fractureds to determine their value
# TODO: Plot fractured versus implicit value 
# TODO maybe fetch result pagesa ll in one request to half dossing
# TODO: Create list of fractured mods that dont do anything
full_search()
