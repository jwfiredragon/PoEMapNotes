import configparser
import csv
import keyboard
import math
import pyperclip
import re
import shutil
import tailer
import tkinter as tk
import utils as u
from pynput.keyboard import Key, Controller
from tempfile import NamedTemporaryFile

DATA_FILE = 'map_notes.csv'
MAP_NOTE_HOTKEY = ''
GENERAL_NOTE_HOTKEY = ''
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
OPEN_ON_ENTER = False
CLIENT_PATH = ''

# https://stackoverflow.com/questions/50570446/python-tkinter-hide-and-show-window-via-hotkeys
class App(tk.Tk):
	new_note = ''
	map_name = ''
	last_map = ''

	def __init__(self):
		super().__init__()
		self.geometry('400x200')
		self.title('Main frame')
		self.editor = tk.Text(self, width = math.floor(WINDOW_WIDTH/8), height = math.floor((WINDOW_HEIGHT-30)/16))
		self.editor.pack()
		self.button = tk.Button(self, text = 'Save and close', command = self.close)
		self.button.pack()
		self.withdraw()

		keyboard.add_hotkey(MAP_NOTE_HOTKEY, self.open_map)
		keyboard.add_hotkey(GENERAL_NOTE_HOTKEY, self.open_general)

	def open_map(self):
		# Using pynput to send keys since keyboard.send is async and runs too late
		Controller().press(Key.ctrl)
		Controller().press('c')
		Controller().release(Key.ctrl)
		Controller().release('c')

		self.map_name = u.parse_map_name(pyperclip.paste())
		self.render()

	def open_general(self):
		self.map_name = 'General Notes'
		self.render()

	def render(self, suppress_not_found = False):
		u.position_window(self, WINDOW_WIDTH, WINDOW_HEIGHT)

		if not re.search('Error:', self.map_name):
			with open(DATA_FILE, 'r') as csv_file:
				reader = csv.reader(csv_file)
				map_found = False

				for row in reader:
					if re.search('^{}$'.format(self.map_name), row[0]):
						map_found = True
						u.render_window(self, self.editor, row[0], row[1])

				if not map_found:
					if suppress_not_found:
						return
					else:
						u.render_window(self, self.editor, 'Error', 'Error: Map not found.')

		else:
			u.render_window(self, self.editor, 'Error', self.map_name)

		self.update()
		self.deiconify()
		self.editor.focus()

	def close(self):
		self.new_note = self.editor.get('1.0', 'end-1c')

		if not re.search('Error:', self.new_note):
			temp_file = NamedTemporaryFile('w+t', newline = '', delete = False)

			with open(DATA_FILE, 'r') as csv_file, temp_file:
				reader = csv.reader(csv_file)
				writer = csv.writer(temp_file)

				for row in reader:
					if re.search('^{}$'.format(self.map_name), row[0]):
						writer.writerow([row[0], self.new_note])
					else:
						writer.writerow(row)

			shutil.move(temp_file.name, DATA_FILE)

		self.new_note = ''
		self.update()
		self.withdraw()
	
	def process_client_txt(self):
		# https://stackoverflow.com/questions/62241472/using-python-and-tkinter-how-would-i-run-code-every-loop-of-mainloop
		with open(CLIENT_PATH, 'r', encoding = 'utf8') as client_txt:
			lines = tailer.tail(client_txt, 2)

			if re.search('You have entered', lines[1]):
				map_name = lines[1].split('entered ')[1].replace('.', '')
				if not map_name == self.last_map:
					self.last_map = map_name
					self.map_name = map_name
					self.render(True)

		self.after(100, self.process_client_txt)

def read_config():
	global MAP_NOTE_HOTKEY, GENERAL_NOTE_HOTKEY, WINDOW_WIDTH, WINDOW_HEIGHT, OPEN_ON_ENTER, CLIENT_PATH

	config = configparser.ConfigParser()
	config.read('config.ini')

	MAP_NOTE_HOTKEY = config.get('Hotkeys', 'open_map_note')
	GENERAL_NOTE_HOTKEY = config.get('Hotkeys', 'open_general_note')
	WINDOW_WIDTH = config.getint('Window', 'width')
	WINDOW_HEIGHT = config.getint('Window', 'height')
	OPEN_ON_ENTER = config.getboolean('Other', 'open_on_enter_map')
	CLIENT_PATH = config.get('Other', 'client_txt_path')

if __name__ == '__main__':
	u.gen_config()
	u.gen_map_list()
	read_config()

	app = App()
	if OPEN_ON_ENTER:
		app.after(100, app.process_client_txt)
	app.mainloop()
