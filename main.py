import tkinter as tk
from gui.ui import GenUI
from settings import Settings

"""Top-level script to call the UI and handle program flow"""

# Instanciate settings
s = Settings()

# Call UI
root = tk.Tk()
ui_app = GenUI(master=root)
ui_app.mainloop()

# When app exits save user settings
user_settings = ui_app.get_user_settings()
s.store_user_settings(user_settings)
