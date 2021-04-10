import csv
import keyboard
import pyperclip
import re
import shutil
import tkinter as tk
import utils as u
from pynput.keyboard import Key, Controller
from tempfile import NamedTemporaryFile

data_file = 'map_notes.csv'

# https://stackoverflow.com/questions/50570446/python-tkinter-hide-and-show-window-via-hotkeys
class App(tk.Tk):
	new_note = ''
	map_name = ''

	def __init__(self):
		super().__init__()
		self.geometry("400x200")
		self.title("Main frame")

		self.editor = tk.Text(self, height=10)
		self.editor.pack()
		self.button = tk.Button(self, text = 'Save and close', command = self.close)
		self.button.pack()
		self.withdraw()

		keyboard.add_hotkey('ctrl+shift+q', self.open_map)
		keyboard.add_hotkey('ctrl+shift+a', self.open_note)

	def open_map(self):
		# Using pynput to send keys since keyboard.send is async and runs too late
		Controller().press(Key.ctrl)
		Controller().press('c')
		Controller().release(Key.ctrl)
		Controller().release('c')

		self.map_name = u.parse_map_name(pyperclip.paste())
		self.render()

	def open_note(self):
		self.map_name = 'General Notes'
		self.render()

	def render(self):
		u.position_window(self, 400, 200)

		if not re.search('Error:', self.map_name):
			with open(data_file, 'r') as csv_file:
				reader = csv.reader(csv_file)
				map_found = False

				for row in reader:
					if re.search(row[0], '^{}$'.format(self.map_name)):
						map_found = True
						u.render_window(self, self.editor, row[0], row[1])

				if map_found == False:
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

			with open(data_file, 'r') as csv_file, temp_file:
				reader = csv.reader(csv_file)
				writer = csv.writer(temp_file)

				for row in reader:
					if re.search(row[0], '^{}$'.format(self.map_name)):
						writer.writerow([row[0], self.new_note])
					else:
						writer.writerow(row)

			shutil.move(temp_file.name, data_file)

		self.new_note = ''
		self.update()
		self.withdraw()

u.gen_map_list()

if __name__ == "__main__":
	App().mainloop()
