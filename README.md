# PoEMapNotes

A little utility to put notes on your maps. Will add features as I think of them if I'm not lazy.

## Instructions

* Download the [latest release](https://github.com/jwfiredragon/PoEMapNotes/releases/) and place it wherever. If updating, simply replace the existing `main.exe`.
* Run `main.exe`. On the first startup, wait for it to generate `map_notes.csv` and `config.ini`. This may take a few seconds.
* Ingame, press CTRL+SHIFT+C while mousing over a map to access its notes, or press CTRL+SHIFT+X to open a general notes window.
	* Note: If you are having trouble with getting the hotkeys to work, try running the app as an administrator.
* Type your notes the text box. They will be saved automatically.
* To hide the window, click the 'Close' button at the bottom. To actually shut down the utility, click the X in the upper right.
* `config.ini` settings:
	* Hotkeys: set hotkeys for various actions. Special keys should be typed out literally in all lowercase ('ctrl', 'shift', 'alt'). Join keys with '+'.
	* Window: `width` and `height` are the window size in pixels.
	* If `fixed_location` is true, the window will open at [`fixed_x`, `fixed_y`] (coordinates on your screen, in pixels). The window will open at cursor location if false.
	* `focus_on_open` will automatically focus your cursor to the notes window when it opens if true.
	* `font_size` is the font size for the window's text.
	* `open_on_enter` automatically opens the map's note on entering a map if true.
	* `client_txt_path` is the full path to your client.txt file, without quotation marks.

## Security

Windows antivirus may flag this as a suspicious app. I promise it's safe, you can manually approve it. If you're paranoid, you can compile from the source code yourself by downloading the repository and running `pyinstaller --onefile --noconsole main.py` in a command terminal. Note that this requires you to have pyinstaller and all requisite librarires installed. `gen_dist.bat` compiles the app with pyinstaller, but first runs `gen_data_dev.py`, which pulls all the necessary map data from [RePoE](https://github.com/brather1ng/RePoE) and [the trade api](https://www.pathofexile.com/api/trade/data/items) into `map_data.py`.

## Planned features

No guarantee on when any of these will be finished.

* Notes on individual items (for Harvest crafting and such)

## Images

Map notes window
![](image.png?raw=true)
