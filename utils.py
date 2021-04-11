import configparser
import csv
import map_data
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
			return 'Error: Not a map.'
	except IndexError:
		return 'Error: Failed to parse map.'

	# strip prefix/suffix as necessary
	if re.search('Magic', map_parse[0]):
		for prefix in map_data.PREFIX_LIST:
			if map_name.split(' ')[0] == prefix:
				map_name = map_name.replace(prefix + ' ', '')
				break
	map_name = map_name.replace('Superior ', '')
	map_name = map_name.split(' Map')[0]

	return map_name

def render_window(root, window, title, text):
	root.title('PoE Map Notes: ' + title)
	window.delete('1.0', tk.END)
	window.insert(tk.END, text)

def position_window(root, width, height):
	mouse_pos = root.winfo_pointerxy()
	screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]

	window_pos = [0, max(mouse_pos[1] - height - 10, 0)]
	if mouse_pos[0] + width/2 < screen_size[0] and mouse_pos[0] - width/2 > 0:
		window_pos[0] = mouse_pos[0] - width/2
	elif mouse_pos[0] + width/2 >= screen_size[0]:
		window_pos[0] = screen_size[0] - width

	root.geometry('%dx%d+%d+%d' %(width, height, window_pos[0], window_pos[1]))

def gen_config():
	config_default = [['Hotkeys', 'open_map_note', 'ctrl+shift+c'],
					  ['Hotkeys', 'open_general_note', 'ctrl+shift+x'],
					  ['Window', 'width', '400'],
					  ['Window', 'height', '200'],
					  ['Other', 'open_on_enter_map', 'true'],
					  ['Other', 'client_txt_path', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Path of Exile\\logs\\Client.txt']]

	if not os.path.isfile('config.ini'):
		config_file = open('config.ini', 'w')
		config_file.close()

	config = configparser.ConfigParser()
	config.read('config.ini')

	for option in config_default:
		if not config.has_option(option[0], option[1]):
			if not config.has_section(option[0]):
				config.add_section(option[0])
			config.set(option[0], option[1], option[2])

	with open('config.ini', 'w') as configfile:
		config.write(configfile)


def gen_map_list():
	if not os.path.isfile('map_notes.csv'):
		new_note_file = open('map_notes.csv', 'w')
		new_note_file.close()

	# https://stackoverflow.com/questions/16020858/inline-csv-file-editing-with-python/16020923#16020923
	note_file_name = 'map_notes.csv'
	temp_file = NamedTemporaryFile('w+', newline = '', delete = False)

	with open(note_file_name, 'r', newline = '') as note_file, temp_file:
		reader = csv.reader(note_file)
		writer = csv.writer(temp_file)
		map_list_curr = []

		for row in reader:
			map_list_curr.append(row[0])
			writer.writerow(row)

		map_list_diff = [map for map in map_data.MAP_LIST if map not in map_list_curr]
		for map in map_list_diff:
			writer.writerow([map, ''])

	shutil.move(temp_file.name, note_file_name)
