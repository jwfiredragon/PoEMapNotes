import re

def parse_map_name(map_raw):
	map_parse = map_raw.split("\n")

	if re.search("Map", map_parse[1]):
		map_name = map_parse[1]
	elif re.search("Map", map_parse[2]):
		map_name = map_parse[2]
	else:
		map_name = "Error: Not a map"
	return map_name