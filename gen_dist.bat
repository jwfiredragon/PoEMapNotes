cd ../RePoE
git pull
cd ../PoEMapNotes
python gen_data_dev.py
pyinstaller --onefile --noconsole main.py
pause