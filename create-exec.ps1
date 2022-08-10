Remove-Item dist/main.exe
Remove-Item main.exe
pyinstaller main.py --onefile --icon=gui\icon.ico
Copy-Item dist/main.exe .
