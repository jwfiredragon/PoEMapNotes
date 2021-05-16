import json
import re
from RePoE import mods

maps_json = None

# items json taken from https://www.pathofexile.com/api/trade/data/items
with open('items.json') as items:
	item_json = json.load(items)
	for result in item_json['result']:
		if result['id'] == 'maps':
			maps_json = result['entries']
			break

map_list = []
unique_map_list = {}
prefix_list = []

# generate list of map names (including unique maps)
for map in maps_json:
	if re.search('Map', map['type']):
		if 'flags' in map and map['flags']['unique']:
			# encode/decode just to handle Maelstr�m of Chaos (evil)
			map_name = map['name'].encode('utf-8').decode('cp1252')
		else:
			map_name = map['type'].split(' Map')[0]
			map_name = map_name.replace('Shaped ', '')
		if map_name not in map_list:
			map_list.append(map_name)
map_list.append('General Notes')
map_list.sort()

# generate dictionary of unique map names vs map types for lookup of unidentified unique maps
for map in maps_json:
	if 'flags' in map and map['flags']['unique']:
		if not re.search('Replica', map['name']):
			map_base = map['type'].split(' Map')[0]
			unique_map_list[map_base] = map['name'].encode('utf-8').decode('cp1252')

# generate list of map prefixes
for mod in mods.values():
	if mod['domain'] == 'area' and mod['generation_type'] == 'prefix' and mod['name'] not in prefix_list:
		prefix_list.append(mod['name'])
prefix_list.sort()

with open('map_data.py', 'w') as data_file:
	data_file.write("MAP_LIST = {}\n".format(map_list))
	data_file.write("UNIQUE_MAP_LIST = {}\n".format(unique_map_list))
	data_file.write("PREFIX_LIST = {}\n".format(prefix_list))
