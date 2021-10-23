import json
import re
from RePoE import mods

MAPS_JSON = None

# items json taken from https://www.pathofexile.com/api/trade/data/items
with open('items.json') as items:
	ITEM_JSON = json.load(items)
	for result in ITEM_JSON['result']:
		if result['id'] == 'maps':
			MAPS_JSON = result['entries']
			break

MAP_LIST = []
UNIQUE_MAP_LIST = {}
PREFIX_LIST = []

# generate list of map names (including unique maps)
for map_ in MAPS_JSON:
	if re.search('Map', map_['type']):
		if 'flags' in map_ and map_['flags']['unique']:
			# encode/decode just to handle Maelstr�m of Chaos (evil)
			map_name = map_['name'].encode('utf-8').decode('cp1252')
		else:
			map_name = map_['type'].split(' Map')[0]
			map_name = map_name.replace('Shaped ', '')
		if map_name not in MAP_LIST:
			MAP_LIST.append(map_name)
MAP_LIST.append('General Notes')
MAP_LIST.sort()

# generate dictionary of unique map names vs map types for lookup of unidentified unique maps
for map_ in MAPS_JSON:
	if 'flags' in map_ and map_['flags']['unique']:
		if not re.search('Replica', map_['name']):
			map_base = map_['type'].split(' Map')[0]
			UNIQUE_MAP_LIST[map_base] = map_['name'].encode('utf-8').decode('cp1252')

# generate list of map prefixes
for mod in mods.values():
	if mod['domain'] == 'area' and mod['generation_type'] == 'prefix' and mod['name'] not in PREFIX_LIST:
		PREFIX_LIST.append(mod['name'])
PREFIX_LIST.sort()

with open('map_data.py', 'w') as data_file:
	data_file.write("MAP_LIST = {}\n".format(MAP_LIST))
	data_file.write("UNIQUE_MAP_LIST = {}\n".format(UNIQUE_MAP_LIST))
	data_file.write("PREFIX_LIST = {}\n".format(PREFIX_LIST))
