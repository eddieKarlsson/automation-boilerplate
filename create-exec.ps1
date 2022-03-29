rm dist/main.exe
rm main.exe
pyinstaller main.py --onefile
cp dist/main.exe .
