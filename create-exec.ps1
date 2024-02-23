Remove-Item dist/main.exe
Remove-Item main.exe
py -m PyInstaller main.py --onefile --icon=gui\icon.ico
Copy-Item dist/main.exe .
