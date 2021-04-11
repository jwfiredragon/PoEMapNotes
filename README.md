# PoEMapNotes

A little utility to put notes on your maps. Will add features as I think of them if I'm not lazy.

## Instructions

* Download the latest release and unzip to wherever. If updating, just replace the existing files, it won't delete your existing notes/config.
* Run main.exe. On the first startup, wait for it to generate `map_notes.csv` and `config.ini`. This may take a few seconds.
* Ingame, press CTRL+SHIFT+Q while mousing over a map to access its notes, or press CTRL+SHIFT+A to open a general notes window.
* Type your notes the text box and click the 'Save and Close' button to close the window.
* To actually shut down the utility altogether, click the X in the upper right of the window.
* `config.ini` settings:
	* Hotkeys: set hotkeys for various actions. Special keys should be typed out literally in all lowercase ('ctrl', 'shift', 'alt'). Join keys with '+'.
	* Window: window size in pixels.
	* `open_on_enter` automatically opens the map's note on entering a map. Defaults to false.
	* `client_txt_path` is the full path to your client.txt file, without quotation marks.

## Security

Windows antivirus may flag this as a suspicious app. I promise it's safe, you can manually approve it. If you're paranoid, you can compile from the source code yourself by downloading the repository and running `gen_dist.bat`. Note that this requires you to have RePoE, pyinstaller, etc. all installed.

## Planned features

No guarantee on when any of these will be finished.

* Proper handling for unique maps
* Notes on individual items (for Harvest crafting and such)

## Images

Map notes window
![](image.png?raw=true)
