import configparser
import csv
import re
import shutil
import tkinter as tk
import tkinter.font as tkf
from tempfile import NamedTemporaryFile
from pynput.keyboard import Key, Controller
import keyboard
import pyperclip
import tailer
import map_data
import utils as u

DATA_FILE = 'map_notes.csv'
MAP_NOTE_HOTKEY = 'ctrl+shift+c'
GENERAL_NOTE_HOTKEY = 'ctrl+shift+x'
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
FIXED_LOCATION = False
FL_X = 0
FL_Y = 0
FONT_SIZE = 10
OPEN_ON_ENTER = True
CLIENT_PATH = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Path of Exile\\logs\\Client.txt'
FOCUS_ON_OPEN = True

# https://stackoverflow.com/questions/50570446/python-tkinter-hide-and-show-window-via-hotkeys
class App(tk.Tk):
	"""The main window of the application"""
	new_note = ''
	map_name = ''
	last_zone = ''
	font = None

	def __init__(self):
		super().__init__()
		self.geometry('400x200')
		self.title('Main frame')
		self.font = tkf.Font(size=FONT_SIZE)
		self.button = tk.Button(self, text='Close', command=self.close)
		self.button.pack(side=tk.BOTTOM)
		self.editor = tk.Text(self, font=self.font)
		self.editor.pack(fill=tk.BOTH)
		self.withdraw()

		keyboard.add_hotkey(MAP_NOTE_HOTKEY, self.open_map)
		keyboard.add_hotkey(GENERAL_NOTE_HOTKEY, self.open_general)

	def open_map(self):
		"""Ctrl+Cs the map on the cursor and shows the main window"""
		# Using pynput to send keys since keyboard.send is async and runs too late
		Controller().press(Key.ctrl)
		Controller().press('c')
		Controller().release(Key.ctrl)
		Controller().release('c')

		self.map_name = u.parse_map_name(pyperclip.paste())
		self.render()

	def open_general(self):
		"""Shows the main window for general note-taking"""
		self.map_name = 'General Notes'
		self.render()

	def render(self):
		"""Shows the main window with the specified position and text"""
		u.position_window(self, WINDOW_WIDTH, WINDOW_HEIGHT, FIXED_LOCATION, FL_X, FL_Y)

		if not re.search('Error', self.map_name):
			if self.map_name in map_data.MAP_LIST:
				with open(DATA_FILE, 'r') as csv_file:
					reader = csv.reader(csv_file)

					for row in reader:
						if re.search('^{}$'.format(self.map_name), row[0]):
							u.render_window(self, self.editor, row[0], row[1])
							break

			else:
				u.render_window(self, self.editor, 'Error', 'Error: Map not found.')

		else:
			u.render_window(self, self.editor, 'Error', self.map_name)

		self.update()
		self.deiconify()
		if FOCUS_ON_OPEN:
			self.editor.focus()

	def close(self):
		"""Hides the main window"""
		self.update()
		self.withdraw()

	def update_note(self):
		"""Checks if the map note in the window has been changed, and updates the map note spreadsheet if so"""
		self.new_note = self.editor.get('1.0', 'end-1c')

		if not re.search('Error', self.title()):
			update_note = False

			with open(DATA_FILE, 'r') as csv_file:
				reader = csv.reader(csv_file)

				for row in reader:
					if re.search('^{}$'.format(self.map_name), row[0]):
						if not re.search('^{}$'.format(self.new_note), row[1]):
							update_note = True

			if update_note:
				temp_file = NamedTemporaryFile('w+t', newline='', delete=False)

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
		self.after(100, self.update_note)

	def process_client_txt(self):
		"""Checks client.txt to see if the player has entered a map"""
		# https://stackoverflow.com/questions/62241472/using-python-and-tkinter-how-would-i-run-code-every-loop-of-mainloop
		with open(CLIENT_PATH, 'r', encoding='utf8', errors='ignore') as client_txt:
			lines = tailer.tail(client_txt, 6)

			for line in lines:
				if re.search('You have entered', line):
					zone_name = line.split('entered ')[1].replace('.', '')
					if not self.last_zone == zone_name:
						self.last_zone = zone_name
						if zone_name in map_data.MAP_LIST:
							self.map_name = zone_name
							self.render()
							break

		self.after(100, self.process_client_txt)

def read_config():
	"""Reads config options from the config file into global variables"""
	global MAP_NOTE_HOTKEY, GENERAL_NOTE_HOTKEY, WINDOW_WIDTH, WINDOW_HEIGHT, FIXED_LOCATION, FL_X, FL_Y, FONT_SIZE, OPEN_ON_ENTER, CLIENT_PATH, FOCUS_ON_OPEN

	config = configparser.ConfigParser()
	config.read('config.ini')

	MAP_NOTE_HOTKEY = config.get('Hotkeys', 'open_map_note')
	GENERAL_NOTE_HOTKEY = config.get('Hotkeys', 'open_general_note')
	WINDOW_WIDTH = config.getint('Window', 'width')
	WINDOW_HEIGHT = config.getint('Window', 'height')
	FIXED_LOCATION = config.getboolean('Window', 'fixed_location')
	FL_X = config.getint('Window', 'fixed_x')
	FL_Y = config.getint('Window', 'fixed_y')
	FONT_SIZE = config.getint('Other', 'font_size')
	OPEN_ON_ENTER = config.getboolean('Other', 'open_on_enter_map')
	CLIENT_PATH = config.get('Other', 'client_txt_path')
	FOCUS_ON_OPEN = config.getboolean('Other', 'focus_on_open')

if __name__ == '__main__':
	u.gen_config()
	u.gen_map_list()
	read_config()

	APP = App()
	APP.after(100, APP.update_note)
	if OPEN_ON_ENTER:
		APP.after(100, APP.process_client_txt)
	APP.mainloop()
