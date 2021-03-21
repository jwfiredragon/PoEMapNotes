import csv
from RePoE import base_items

# needed as a separate file because pyinstaller doesn't bundle RePoE

map_list = []

for base_item in base_items.values():
	if base_item['item_class'] == 'Map':
		if base_item['name'].split(' ')[0] != 'Shaped':
			map_list.append(base_item['name'].split(' Map')[0])
# remove duplicate values
map_list = list(set(map_list))

data_file = open('map_data.csv', 'w', newline = '')
writer = csv.writer(data_file)

for map in map_list:
	writer.writerow([map])
