pyinstaller main.py --onefile
timeout 2
robocopy .\dist .\ main.exe /move
timeout 2
rmdir /s /q .\build
rmdir /s /q .\dist
del .\main.spec