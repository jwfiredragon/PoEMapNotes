import csv
import os
import shutil
from RePoE import base_items
from tempfile import NamedTemporaryFile

map_list_data = []
map_list_curr = []

for base_item in base_items.values():
	if base_item["item_class"] == "Map":
		if base_item["name"].split(" ")[0] != "Shaped":
			map_list_data.append(base_item["name"].split(" Map")[0])
# remove duplicate values
map_list_data = list(set(map_list_data))

if not os.path.isfile("map_notes.csv"):
	new_data_file = open("map_notes.csv", "w")
	new_data_file.close()

# https://stackoverflow.com/questions/16020858/inline-csv-file-editing-with-python/16020923#16020923
data_file = "map_notes.csv"
temp_file = NamedTemporaryFile("w+", newline = '', delete = False)

with open(data_file, "r", newline = '') as csvFile, temp_file:
	reader = csv.reader(csvFile, delimiter = ',')
	writer = csv.writer(temp_file, delimiter = ',')

	for row in reader:
		map_list_curr.append(row[0])
		writer.writerow(row)

	map_list_diff = [map for map in map_list_data if map not in map_list_curr]
	for map in map_list_diff:
		writer.writerow([map, ""])

shutil.move(temp_file.name, data_file)