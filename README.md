# Automation-boilerplate
## Creates importable text files from boilerplate code. Purpose is to speed up automation projects by generating repetetive code for each specified item in item-list.

Run the program from terminal by invoking main.py or run the main.exe if you're on Windows.

Requirements:
1. pip install openpyxl
2. Item-list with layout like example_td.xlsx

Create executable using https://www.pyinstaller.org/:
Run create-exec.ps1 or do the steps manually:
1. pip install pyinstaller
2. cd to github folder
3. pyinstaller main.py --onefile
4. Move dist\main.exe to main folder, then relative path will work
