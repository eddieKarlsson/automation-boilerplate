import tkinter
import tkinter.messagebox
import tkinter.filedialog as filedialog
import customtkinter
import os
import os.path
from settings import Settings
from gen_main import GenMain

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GenUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.s = Settings()

        # Constants
        self.height = 530
        self.width = 900

        self.resizable(False,False)
        
        # Get Current User Data
        self.user_settings = self.get_user_settings()

        self.create_window()
        self.create_window_contents()
        #self.create_dropdown()

        # "Run Script" button changes state from this function
        self.check_path_validity()

    def create_window(self):
        # configure window
        self.title("automation-boilerplate")
        self.geometry(f"{self.width}x{self.height}")

    def create_dropdown(self):
        """Create drop-down menu"""
        self.menu = customtkinter.Menu(self.master)
        self.master.config(menu=self.menu)

        # file submenu
        self.subMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Exit", command=self.master.quit)

        # view submenu
        self.viewSubMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.viewSubMenu)
        self.viewSubMenu.add_command(label="Config path",
                                     command=self.open_config_path)

        # about submenu
        self.aboutSubMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="About", menu=self.aboutSubMenu)
        self.aboutSubMenu.add_command(label="Version",
                                      command=self.create_about_window)

    def create_window_contents(self):
        """Create window contents"""

        # create header
        self.header = customtkinter.CTkFrame(self, corner_radius=0, height=0)
        self.header.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.headerlabel = customtkinter.CTkLabel(self.header, text="automation-boilerplate", font=customtkinter.CTkFont(size=20, weight="bold"), anchor=customtkinter.W)
        self.headerlabel.grid(row=0, column=0, padx=10, pady=10)

        # create filesheader
        self.filesheader = customtkinter.CTkFrame(self, corner_radius=0)
        self.filesheader.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.filesheaderlabel = customtkinter.CTkLabel(self.filesheader, text="Välj filer och mappar", font=customtkinter.CTkFont(size=20, weight="bold"), anchor=customtkinter.W)
        self.filesheaderlabel.grid(row=1, column=0, padx=10, pady=10)

        # create files
        self.files = customtkinter.CTkFrame(self, corner_radius=0)
        self.files.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")      

        # Excel button
        self.excelButton = customtkinter.CTkButton(self.files, command=self.browse_excel, text="Välj  TD")
        self.excelButton.grid(row=1, column=0, padx=20, pady=10)

        # Excel path label
        self.excelLabel = customtkinter.CTkLabel(self.files, text=(self.user_settings['excel_path']))
        self.excelLabel.grid(row=1, column=1, padx=20, pady=10)

        # Output button
        self.outpathButton = customtkinter.CTkButton(self.files, command=self.output_path, text="Välj utmatnings mapp")
        self.outpathButton.grid(row=2, column=0, padx=20, pady=10)

        # Output path label
        self.outpathLabel = customtkinter.CTkLabel(self.files, text=(self.user_settings['output_path']))
        self.outpathLabel.grid(row=2, column=1, padx=20, pady=10)

        # config path button
        if self.s.SHOW_CONFIG_ROW:
            self.cfgpathButton = customtkinter.CTkLabel(self.files, text="Config path...", command=self.config_path)
            self.cfgpathButton.grid(row=3, column=0, padx=20, pady=10)

            # config path label
            self.cfgpathLabel = customtkinter.CTkLabel(self.files, text=(self.user_settings['config_path']))
            self.cfgpathLabel.grid(row=3, column=1, padx=20, pady=10)

        # create configsheader
        self.configsheader = customtkinter.CTkFrame(self, corner_radius=0)
        self.configsheader.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.configsheaderlabel = customtkinter.CTkLabel(self.configsheader, text="Välj vad som inte ska genereras", font=customtkinter.CTkFont(size=20, weight="bold"), anchor=customtkinter.W)
        self.configsheaderlabel.grid(row=1, column=0, padx=10, pady=10)

        # create configs
        self.configs = customtkinter.CTkFrame(self, corner_radius=0)
        self.configs.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        self.valve_var = customtkinter.BooleanVar()
        self.valve_var.initialize(self.user_settings['VALVE_DISABLE'])
        self.valve_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.valve_var, text="Disable VALVE generation")
        self.valve_disabled.grid(row=5, column=0, pady=(20, 10), padx=20, sticky="n")

        self.motor_var = customtkinter.BooleanVar()
        self.motor_var.initialize(self.user_settings['MOTOR_DISABLE'])
        self.motor_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.motor_var, text="Disable MOTOR generation")
        self.motor_disabled.grid(row=5, column=1, pady=(20, 10), padx=20, sticky="n")

        self.di_var = customtkinter.BooleanVar()
        self.di_var.initialize(self.user_settings['DI_DISABLE'])
        self.di_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.di_var, text="Disable DI generation")
        self.di_disabled.grid(row=5, column=2, pady=(20, 10), padx=20, sticky="n")

        self.do_var = customtkinter.BooleanVar()
        self.do_var.initialize(self.user_settings['DO_DISABLE'])
        self.do_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.do_var, text="Disable DO generation")
        self.do_disabled.grid(row=5, column=3, pady=(20, 10), padx=20, sticky="n")

        self.ai_var = customtkinter.BooleanVar()
        self.ai_var.initialize(self.user_settings['AI_DISABLE'])
        self.ai_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.ai_var, text="Disable AI generation")
        self.ai_disabled.grid(row=6, column=0, pady=(20, 10), padx=20, sticky="n")

        self.ao_var = customtkinter.BooleanVar()
        self.ao_var.initialize(self.user_settings['AO_DISABLE'])
        self.ao_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.ao_var, text="Disable AO generation")
        self.ao_disabled.grid(row=6, column=1, pady=(20, 10), padx=20, sticky="n")

        self.pid_var = customtkinter.BooleanVar()
        self.pid_var.initialize(self.user_settings['PID_DISABLE'])
        self.pid_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.pid_var, text="Disable PID generation")
        self.pid_disabled.grid(row=6, column=2, pady=(20, 10), padx=20, sticky="n")

        self.sum_var = customtkinter.BooleanVar()
        self.sum_var.initialize(self.user_settings['SUM_DISABLE'])
        self.sum_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.sum_var, text="Disable SUM generation")
        self.sum_disabled.grid(row=6, column=3, pady=(20, 10), padx=20, sticky="n")

        self.alarm_var = customtkinter.BooleanVar()
        self.alarm_var.initialize(self.user_settings['ALARM_DISABLE'])
        self.alarm_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.alarm_var, text="Disable ALARM generation")
        self.alarm_disabled.grid(row=7, column=0, pady=(20, 10), padx=20, sticky="n")

        self.asi_var = customtkinter.BooleanVar()
        self.asi_var.initialize(self.user_settings['ASI_DISABLE'])
        self.asi_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.asi_var, text="Disable ASI generation")
        self.asi_disabled.grid(row=7, column=1, pady=(20, 10), padx=20, sticky="n")

        self.units_var = customtkinter.BooleanVar()
        self.units_var.initialize(self.user_settings['UNITS_DISABLE'])
        self.units_disabled = customtkinter.CTkCheckBox(master=self.configs, variable=self.units_var, text="Disable UNITS generation")
        self.units_disabled.grid(row=7, column=2, pady=(20, 10), padx=20, sticky="n")

        # Run script
        self.runButton = customtkinter.CTkButton(self.configs, text="Generera", command=self.run_self, state=customtkinter.DISABLED)
        self.runButton.grid(row=10, column=0, padx=20, pady=10)
    
    def browse_excel(self):
        excelPath = filedialog.askopenfilename(
            filetypes=(("Excel files",
                        "*.xlsx"),
                       ("all files", "*.*")))

        # Write to user_settings dictionary, to save it for later.
        self.user_settings['excel_path'] = excelPath
        # Update label
        self.excelLabel.configure(text=excelPath)

        # Check if all path are valid
        self.check_path_validity()

    def output_path(self):
        output_path = filedialog.askdirectory()
        # Write to user_settings dictionary, to save it for later.
        self.user_settings['output_path'] = output_path
        # Update label
        self.outpathLabel.configure(text=output_path)

    def config_path(self):
        config_path = filedialog.askdirectory()
        # Write to user_settings dictionary, to save it for later.
        self.user_settings['config_path'] = config_path
        # Update label
        self.cfgpathLabel.configure(text=config_path)

    def check_path_validity(self):
        if os.path.isfile(self.user_settings['excel_path']):
            self.runButton.configure(state=customtkinter.NORMAL)
        else:
            self.runButton.configure(state=customtkinter.DISABLED)

    def run_self(self):
        self.check_disable_buttons()
        self.s.store_user_settings(self.user_settings)
        GenMain()

    def open_config_path(self):
        c_path = self.user_settings['config_path']
        c2_path = os.path.realpath(c_path)
        os.startfile(c2_path)

    def create_about_window(self):
        self.about = customtkinter.Toplevel()
        self.about.title('About')
        self.label = customtkinter.Label(self.about, text=self.s.version).pack()

    def get_user_settings(self):
        return self.s.user_settings

    def check_disable_buttons(self):
        self.user_settings['VALVE_DISABLE'] = self.valve_var.get()
        self.user_settings['MOTOR_DISABLE'] = self.motor_var.get()
        self.user_settings['DI_DISABLE'] = self.di_var.get()
        self.user_settings['DO_DISABLE'] = self.do_var.get()
        self.user_settings['AI_DISABLE'] = self.ai_var.get()
        self.user_settings['AO_DISABLE'] = self.ao_var.get()
        self.user_settings['PID_DISABLE'] = self.pid_var.get()
        self.user_settings['SUM_DISABLE'] = self.sum_var.get()
        self.user_settings['ALARM_DISABLE'] = self.alarm_var.get()
        self.user_settings['ASI_DISABLE'] = self.asi_var.get()
        self.user_settings['UNITS_DISABLE'] = self.units_var.get()
        