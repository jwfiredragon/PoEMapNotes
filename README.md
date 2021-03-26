# PoEMapNotes

A little utility to put notes on your maps. Will add features as I think of them if I'm not lazy.

## Instructions

* Download the latest release and unzip to wherever. If updating, just replace the existing files, it won't delete your existing notes.

* Run main.exe. On first startup, wait for it to generate map_notes.csv. May take a few seconds.

* Ingame, press CTRL+SHIFT+Q (currenty not modifiable) while mousing over a map to access its notes. Type whatever you want in the text box and click the 'Save and Close' button to close the window.

* To actually shut down the utility altogether, click the X in the upper right of the window.

## Security

Windows antivirus may flag this as a suspicious app. I promise it's not, you can manually approve it. If you're paranoid, you can compile from the source code yourself by downloading the repository and running `pyinstaller --onefile --noconsole main.py`.

![](image.png?raw=true)