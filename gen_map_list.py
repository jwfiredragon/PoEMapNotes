import csv
import os
import shutil
from tempfile import NamedTemporaryFile

map_list_data = []
map_list_curr = []

map_data_file = open('map_data.csv', 'r')
reader = csv.reader(map_data_file)
for row in reader:
	map_list_data.append(row[0])

if not os.path.isfile('map_notes.csv'):
	new_note_file = open('map_notes.csv', 'w')
	new_note_file.close()

# https://stackoverflow.com/questions/16020858/inline-csv-file-editing-with-python/16020923#16020923
note_file_name = 'map_notes.csv'
temp_file = NamedTemporaryFile('w+', newline = '', delete = False)

with open(note_file_name, 'r', newline = '') as note_file, temp_file:
	reader = csv.reader(note_file)
	writer = csv.writer(temp_file)

	for row in reader:
		map_list_curr.append(row[0])
		writer.writerow(row)

	map_list_diff = [map for map in map_list_data if map not in map_list_curr]
	for map in map_list_diff:
		writer.writerow([map, ''])

shutil.move(temp_file.name, note_file_name)
