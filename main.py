import csv
import pyperclip
import re
import shutil
import tkinter as tk
from tempfile import NamedTemporaryFile
from utils import parse_map_name

new_note = ''
def get_input():
	global new_note
	new_note = note_window.get('1.0', 'end-1c')

note_window_root = tk.Tk()
note_window = tk.Text(note_window_root, height = 10, width = 50)
note_window.pack()
save_button = tk.Button(note_window_root, height = 1, width = 15, text = 'Save and close', command = lambda: [get_input(), note_window_root.destroy()])
save_button.pack()

map_name = parse_map_name(pyperclip.paste())

if not re.search('Error', map_name):
	data_file = 'map_notes.csv'
	temp_file = NamedTemporaryFile('w+t', newline = '', delete = False)

	with open(data_file, 'r') as csvFile, temp_file:
		reader = csv.reader(csvFile)
		writer = csv.writer(temp_file)

		map_found = False
		for row in reader:
			if re.search(row[0], map_name):
				map_found = True

				note_window_root.title('PoE Map Notes: ' + row[0])
				note_window.insert(tk.END, row[1])
				tk.mainloop()
				
				writer.writerow([row[0], new_note if new_note else row[1]])
			else:
				writer.writerow(row)

		if map_found == False:
			note_window_root.title('PoE Map Notes: Error')
			note_window.insert(tk.END, 'Error: Map not found')
			tk.mainloop()

	shutil.move(temp_file.name, data_file)
else:
	note_window_root.title('PoE Map Notes: Error')
	note_window.insert(tk.END, map_name)
	tk.mainloop()
