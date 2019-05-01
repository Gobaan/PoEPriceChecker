import json
import re

def extract_numbers(mod):
    extractor = re.compile(r'\d+')
    numbers = [int(number) for number in extractor.findall(mod)]
    if len(numbers) == 2:
        return numbers
    if len(numbers) == 4:
        return ((numbers[0] + numbers[2])/2, (numbers[1] + numbers[3])/2)
    return (numbers[0], numbers[0])

def get_mod(tier):
    if 'Global' in tier:
        return tier['Global']
    return tier['Local']

def scaled(tier):
    numbers =  extract_numbers(get_mod(tier))
    return [numbers[0], numbers[1]]

def get_best_alt_tier(tiers):
    tiers = [tier for tier in tiers if tier['Tier'].strip()][::-1]
    tiers = tiers[:2]
    return [(
        scaled(tier) + 
        [(100/float(tier['Percent'][:-1])), 
            get_mod(tier),
        ]) 
        for tier in tiers]

def remainder(synth, best_tiers):
    target = synth[0]
    lowest, highest = best_tiers[0][0], best_tiers[0][1]
    return (target - highest * 2) < lowest, target - highest * 2, target - lowest * 2

def get_info(mod_tiers, mod_synth, ignore=[]):
    shared_keys = set(mod_tiers.keys()) & set(mod_synth.keys())
    shared_keys = [key for key in shared_keys if key not in ignore]
    for key in shared_keys:
        best_tiers =  get_best_alt_tier(mod_tiers[key][0])
        t2_allowed, best_case, worst_case = remainder(mod_synth[key], best_tiers)
        if t2_allowed:
            print ('-' * 20)
            print(f"\t'{key}',")
            print (mod_synth[key])
            print (best_tiers)
            print (best_case, worst_case)
          
names = ['ring', 'amulet', 'sceptre', 'wand', 'boots', 'gloves', 'helmet', 'shield']
def generate_ignore():
    # todo auto price check to generate this list
    for name in names:
        print (f"'{name}': [")
        with open(f'data/parsed_{name}.json') as fp:
            combo = json.load(fp)
        print ('\t#prefixes')
        get_info(combo['prefixes'], combo['synth'])
        print ('\t#suffixes')
        get_info(combo['suffixes'], combo['synth'])
        print ('],')

def get_tiers():
    from garbage import ignore
    for name in names:
        print (f"{name}")
        with open(f'data/parsed_{name}.json') as fp:
            combo = json.load(fp)
        print ('#prefixes')
        get_info(combo['prefixes'], combo['synth'], ignore[name])
        print ('#suffixes')
        get_info(combo['suffixes'], combo['synth'], ignore[name])

get_tiers()
