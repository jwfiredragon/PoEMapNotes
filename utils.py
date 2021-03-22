import pynput
import re
import tkinter as tk

def parse_map_name(map_raw):
	map_parse = map_raw.split('\n')

	if re.search('Map', map_parse[1]):
		map_name = map_parse[1]
	elif re.search('Map', map_parse[2]):
		map_name = map_parse[2]
	else:
		map_name = 'Error: Not a map'
	return map_name

def render_window(root, window, title, text):
	root.title('PoE Map Notes: ' + title)
	window.insert(tk.END, text)
	window.focus_set()
	tk.mainloop()

def position_window(root, width, height):
	mouse_pos = pynput.mouse.Controller().position
	screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]
	window_pos = [mouse_pos[0] - width/2 if mouse_pos[0] + width/2 < screen_size[0] else screen_size[0] - width,
				  mouse_pos[1] - height]
	root.geometry('%dx%d+%d+%d' %(width, height, window_pos[0], window_pos[1]))