rm dist/main.exe
rm main.exe
pyinstaller main.py --onefile --icon=gui\icon.ico
cp dist/main.exe .
