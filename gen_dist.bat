cd ../RePoE
git pull
cd ../PoEMapNotes
python gen_map_list_dev.py
xcopy map_data.csv dist
pyinstaller --onefile --noconsole main.py
pyinstaller --onefile --noconsole gen_map_list.py
pause