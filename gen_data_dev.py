import csv
from RePoE import base_items, mods

# needed as a separate file because pyinstaller doesn't bundle RePoE

map_list = []
prefix_list = []

for base_item in base_items.values():
	if base_item['item_class'] == 'Map' and base_item['name'].split(' ')[0] != 'Shaped':
			map_list.append(base_item['name'].split(' Map')[0])
# remove duplicate values
map_list = list(set(map_list))
map_list.append('General Notes')
map_list.sort()

for mod in mods.values():
	if mod['domain'] == 'area' and mod['generation_type'] == 'prefix':
		prefix_list.append(mod['name'])
prefix_list = list(set(prefix_list))
prefix_list.sort()

with open('data.py', 'w') as data_file:
	data_file.write("map_list = {}\n".format(map_list))
	data_file.write("prefix_list = {}\n".format(prefix_list))
