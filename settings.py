import json
import os
import sys


class Settings:
    """A class to store all settings, user-data in JSON format."""

    def __init__(self):
        self.version = 2.0

        """Settings"""
        self.HEADER_ROW = 3  # Excel header
        self.ROW = 6  # Excel start row of data
        self.INDEX_REPLACE = '@INDEX'  # string to be replaced in config file

        # If this variable is set to true, all variables COL_ with integer
        # number will be ignored. the script will instead find the headers
        # by looping through the header and search for the name _NAME.
        self.FIND_HEADERS_AUTOMATICALLY = True

        self.COL_ID_NAME = 'ID'
        self.COL_ID = 2  # Excel column index of ID, 2 = B column
        self.ID_REPLACE = '@ID'  # string to be replaced in config file

        self.COL_COMMENT_NAME = 'Description'
        self.COL_COMMENT = 3  # Excel column index of Comment, 3 = C column
        self.COMMENT_REPLACE = '@CMT'  # string to be replaced in config file

        self.COL_CONFIG_NAME = 'Config'
        self.COL_CONFIG = 7  # Excel column index of Config, 7 = G column
        self.CONFIG_REPLACE = '@CFG'  # string to be replaced in config file

        self.COL_ENG_UNIT_NAME = 'Eng. Unit'
        self.COL_ENG_UNIT = 11  # Excel column index of Config, 11 = K column
        self.ENG_UNIT_REPLACE = '@ENGUNIT'  # string to be replaced

        self.COL_ENG_MIN_NAME = 'Eng. Min'
        self.COL_ENG_MIN = 14  # Excel column index of Config, 14 = O column
        self.ENG_MIN_REPLACE = '@ENGMIN'  # string to be replaced

        self.COL_ENG_MAX_NAME = 'Eng. Max'
        self.COL_ENG_MAX = 15  # Excel column index of Config, 15 = O column
        self.ENG_MAX_REPLACE = '@ENGMAX'  # string to be replaced

        self.COL_ALARM_GROUP_NAME = 'Alarm Group'
        self.COL_ALARM_GROUP = 4  # Excel column index of Config, 15 = O column
        self.ALARM_GROUP_REPLACE = '@AlarmGroup'  # string to be replaced

        self.ADR_REPLACE = '@ADR'  # string to be replaced in config file

        self.COL_PLC_NAME = 'PLC'  # Used in Intouch
        self.COL_PLC = 5  # Excel column index of Config, 15 = O column
        self.PLC_REPLACE = '@PLC'  # string to be replaced in config file

        self.DI_DISABLE = False
        self.DI_START_INDEX = 0  # Start-position index in datablock
        self.DI_SHEETNAME = 'DI'

        self.DO_DISABLE = False
        self.DO_START_INDEX = 0
        self.DO_SHEETNAME = 'DO'

        self.VALVE_DISABLE = False
        self.VALVE_START_INDEX = 0
        self.VALVE_SHEETNAME = 'Valve'

        self.MOTOR_DISABLE = False
        self.MOTOR_START_INDEX = 0
        self.MOTOR_SHEETNAME = 'Motor'

        self.AI_DISABLE = False
        self.AI_START_INDEX = 0
        self.AI_SHEETNAME = 'AI'

        self.AO_DISABLE = False
        self.AO_START_INDEX = 0
        self.AO_SHEETNAME = 'AO'

        self.PID_DISABLE = False
        self.PID_START_INDEX = 0
        self.PID_SHEETNAME = 'PID'

        self.SUM_DISABLE = False
        self.SUM_START_INDEX = 0
        self.SUM_SHEETNAME = 'Sum'

        self.TIA_DIR = 'TIA'
        self.INTOUCH_DIR = 'InTouch'
        self.SQL_DIR = 'SQL'

        # UI
        self.SHOW_CONFIG_ROW = False

        # internal var, used below in functions
        self.json_file = 'user_settings.json'
        self.indent = 1

        # If terminal argument supplied, set debug level
        if len(sys.argv) > 1:
            self.debug_level = int(sys.argv[1])
        else:
            self.debug_level = 0

    def _create_user_settings(self):
        """Create dict which contains all user data"""
        user_settings = {
            'excel_path': 'No excel specified',
            'output_path': 'No path specified',
            'config_path': 'config',
        }

        return user_settings

    def load_user_settings(self):
        """Load stored user settings, otherwise create .json file"""

        # Check if settings file already exists, else create it.
        if os.path.isfile(self.json_file):
            with open(self.json_file, 'r') as f:
                user_settings = json.load(f)
        else:
            user_settings = self._create_user_settings()

            with open(self.json_file, 'w') as f:
                json.dump(user_settings, f, indent=self.indent)

        return user_settings

    def store_user_settings(self, user_settings):
        """Dump Dict to JSON file"""
        with open(self.json_file, 'w') as f:
            json.dump(user_settings, f, indent=self.indent)
