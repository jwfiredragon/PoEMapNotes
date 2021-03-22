cd ../RePoE
git pull
cd ../PoEMapNotes
python gen_map_list_dev.py
xcopy map_data.csv dist /Y
pyinstaller --onefile main.py
pause