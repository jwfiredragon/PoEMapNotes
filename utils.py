import csv
import os
import re
import shutil
import tkinter as tk
from tempfile import NamedTemporaryFile

def parse_map_name(map_raw):
	map_parse = map_raw.split('\n')

	try:
		if re.search('Map', map_parse[1]):
			map_name = map_parse[1]
		elif re.search('Map', map_parse[2]):
			map_name = map_parse[2]
		else:
			map_name = 'Error: Not a map.'
	except IndexError:
		map_name = 'Error: Failed to parse map.'

	return map_name

def render_window(root, window, title, text):
	root.title('PoE Map Notes: ' + title)
	window.delete('1.0', tk.END)
	window.insert(tk.END, text)

def position_window(root, width, height):
	mouse_pos = root.winfo_pointerxy()
	screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]
	window_pos = [0, mouse_pos[1] - height]
	if mouse_pos[0] + width/2 < screen_size[0] and mouse_pos[0] - width/2 > 0:
		window_pos[0] = mouse_pos[0] - width/2
	elif mouse_pos[0] + width/2 >= screen_size[0]:
		window_pos[0] = screen_size[0] - width

	root.geometry('%dx%d+%d+%d' %(width, height, window_pos[0], window_pos[1]))

def gen_map_list():
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