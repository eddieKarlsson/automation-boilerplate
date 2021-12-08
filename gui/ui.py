import tkinter as tk
from tkinter import filedialog
import os
import os.path
from settings import Settings
from gen_main import GenMain


class GenUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.s = Settings()
        self.user_data = self.s.load_user_settings()

        # Constants
        self.height = 275
        self.width = 750
        self.frameColor = "#2b2b2b"
        self.buttonWidth = 0.23
        self.buttonHeight = 0.09
        self.button_bg = "#2b2b2b"
        self.button_fg = "#FFFFFF"  # text color
        self.fontSize = 10
        self.buttonYSpacing = 0.18
        self.checkbuttonYSpacing = 0.1

        # Call app
        self.create_window()
        self.create_window_contents()
        self.create_dropdown()

        # "Run Script" button changes state from this function
        self.check_path_validity()

    def create_window(self):
        """Create window"""
        # Title and program-icon
        self.master.title('automation-boilerplate')
        #  self.master.iconbitmap('icon.ico')
        icon_path = os.path.join('gui', 'icon.png')
        self.master.call('wm', 'iconphoto', self.master._w,
                         tk.PhotoImage(file=icon_path))

        self.canvas = tk.Canvas(self.master, height=self.height,
                                width=self.width)
        self.canvas.pack()
        self.frame = tk.Frame(self.master, bg=self.frameColor)
        self.frame.place(relwidth=1, relheight=1)

    def create_dropdown(self):
        """Create drop-down menu"""
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # file submenu
        self.subMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Exit", command=self.master.quit)

        # view submenu
        self.viewSubMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.viewSubMenu)
        self.viewSubMenu.add_command(label="Settings file",
                                     command=self.open_settings)
        self.viewSubMenu.add_command(label="Config path",
                                     command=self.open_config_path)

        # about submenu
        self.aboutSubMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="About", menu=self.aboutSubMenu)
        self.aboutSubMenu.add_command(label="Version",
                                      command=self.create_about_window)

    def create_window_contents(self):
        """Create window contents"""
        # Excel button
        y = 0.1
        self.excelButton = tk.Button(self.master, text="Select Excel...",
                                     bg=self.button_bg, fg=self.button_fg,
                                     command=self.browse_excel)

        self.excelButton.place(relx=0.03, rely=y,
                               relheight=self.buttonHeight,
                               relwidth=self.buttonWidth)

        # Excel path label
        self.excelLabel = tk.Label(self.frame, bg=self.button_bg,
                                   fg=self.button_fg,
                                   text=(self.user_data['excel_path']))

        self.excelLabel.place(relx=0.27, rely=y, relheight=self.buttonHeight)

        # Output path button
        self.outpathButton = tk.Button(self.master, text="Output path...",
                                       bg=self.button_bg, fg=self.button_fg,
                                       command=self.output_path)
        y += self.buttonYSpacing
        self.outpathButton.place(relx=0.03, rely=y,
                                 relheight=self.buttonHeight,
                                 relwidth=self.buttonWidth)

        # Output path label
        self.outpathLabel = tk.Label(self.frame, bg=self.button_bg,
                                     fg=self.button_fg,
                                     text=(self.user_data['output_path']))

        self.outpathLabel.place(relx=0.27, rely=y,
                                relheight=self.buttonHeight)

        y += self.buttonYSpacing
        # config path button
        self.cfgpathButton = tk.Button(self.master, text="Config path...",
                                       bg=self.button_bg, fg=self.button_fg,
                                       command=self.config_path)

        self.cfgpathButton.place(relx=0.03, rely=y,
                                 relheight=self.buttonHeight,
                                 relwidth=self.buttonWidth)

        # config path label
        self.cfgpathLabel = tk.Label(self.frame, bg=self.button_bg,
                                     fg=self.button_fg,
                                     text=(self.user_data['config_path']))

        self.cfgpathLabel.place(relx=0.27, rely=y,
                                relheight=self.buttonHeight)

        y += self.buttonYSpacing
        y += self.buttonYSpacing
        # Run script
        self.run_self = tk.Button(self.master, text="Run script",
                                  bg=self.button_bg, fg=self.button_fg,
                                  command=self.run_self, state=tk.DISABLED)

        self.run_self.place(relx=0.03, rely=y, relheight=self.buttonHeight,
                            relwidth=self.buttonWidth)

    def browse_excel(self):
        excelPath = filedialog.askopenfilename(
            filetypes=(("Excel files",
                        "*.xlsx"),
                       ("all files", "*.*")))

        # Write to user_data dictionary, to save it for later.
        self.user_data['excel_path'] = excelPath
        # Update label
        self.excelLabel.config(text=excelPath)

        # Check if all path are valid
        self.check_path_validity()

    def output_path(self):
        output_path = filedialog.askdirectory()
        # Write to user_data dictionary, to save it for later.
        self.user_data['output_path'] = output_path
        # Update label
        self.outpathLabel.config(text=output_path)

    def config_path(self):
        config_path = filedialog.askdirectory()
        # Write to user_data dictionary, to save it for later.
        self.user_data['config_path'] = config_path
        # Update label
        self.cfgpathLabel.config(text=config_path)

    def open_settings(self):
        os.system('settings.py')

    def run_python_windows_command(self):
        os.system('run.bat')

    def check_path_validity(self):
        if os.path.isfile(self.user_data['excel_path']):
            self.run_self.configure(state=tk.NORMAL)
        else:
            self.run_self.configure(state=tk.DISABLED)

    def run_self(self):
        GenMain(self.user_data['excel_path'], self.user_data['output_path'],
                self.user_data['config_path'])

    def open_config_path(self):
        c_path = self.user_data['config_path']
        c2_path = os.path.realpath(c_path)
        os.startfile(c2_path)

    def create_about_window(self):
        self.about = tk.Toplevel()
        self.about.title('About')
        self.label = tk.Label(self.about, text=self.s.version).pack()

    def get_user_settings(self):
        return self.user_data
