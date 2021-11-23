import sys
import os
import json
import openpyxl as xl
from settings import Settings
from obj_lib.valve import Valve
from obj_lib.motor import Motor
from obj_lib.di import DI
from obj_lib.do import DO


class GenMain:
    """Main class called from UI,
    read data from excel and then execute sub-class functions
    """
    def __init__(self, excel_path, output_path, config_path):
        self.excel_path = excel_path
        self.output_path = output_path
        self.config_path = config_path
        self.s = Settings()
        self.all_it_files = []  # Create an empty list
        self.dict_list = []

        self.generate()

    def _open_gen_excel(self):
        try:
            wb = xl.load_workbook(self.excel_path, data_only=True)
        except FileNotFoundError as e:
            print(e)
            print('ERROR! Excel file not found, program will exit')
            sys.exit()
        else:
            self.wb = wb

    def copy_excel_data_to_dictionaries(self):
        """Open excel and read all relevant object-data to dict"""
        self._open_gen_excel()

        # Create all dictionaries, if enabled in settings
        if not self.s.DI_DISABLE:
            self.di_dict = self._obj_data_to_dict(
                        self.s.DI_SHEETNAME, self.s.DI_START_INDEX, 'di',
                        config=True)
            self.dict_list.append(self.di_dict)

        if not self.s.DO_DISABLE:
            self.do_dict = self._obj_data_to_dict(
                        self.s.DO_SHEETNAME, self.s.DO_START_INDEX, 'do',
                        config=True)
            self.dict_list.append(self.do_dict)

        if not self.s.VALVE_DISABLE:
            self.valve_dict = self._obj_data_to_dict(
                self.s.VALVE_SHEETNAME, self.s.VALVE_START_INDEX, 'valve',
                config=True)
            self.dict_list.append(self.valve_dict)

        if not self.s.MOTOR_DISABLE:
            self.motor_dict = self._obj_data_to_dict(
                            self.s.MOTOR_SHEETNAME, self.s.MOTOR_START_INDEX,
                            'motor', config=True)
            self.dict_list.append(self.motor_dict)

        if not self.s.AI_DISABLE:
            self.ai_dict = self._obj_data_to_dict(
                self.s.AI_SHEETNAME, self.s.AI_START_INDEX, 'ai',
                eng_var=True)
            self.dict_list.append(self.ai_dict)

        if not self.s.AO_DISABLE:
            self.ao_dict = self._obj_data_to_dict(
                    self.s.AO_SHEETNAME, self.s.AO_START_INDEX, 'ao',
                    eng_var=True)
            self.dict_list.append(self.ao_dict)

    def _obj_data_to_dict(self, sheet, start_index, type,
                          config=False, eng_var=False):
        """Read all object data to dict"""

        # Open excel sheet
        try:
            ws = self.wb[sheet]
        except KeyError:
            msg = f'ERROR! {sheet} sheet does not exist, prog will exit'
            print(msg)
            sys.exit()

        # Set column indexes, automatically or hard-coded
        if self.s.FIND_HEADERS_AUTOMATICALLY:
            # Loop header and set the corresponding variables to
            # the integer number
            for i in range(1, 20):
                cell = ws.cell(row=self.s.HEADER_ROW, column=i)
                cellval = str(cell.value)

                # If cell is empty (NoneType) - skip it
                if cellval is None:
                    continue

                if self.s.COL_ID_NAME in cellval:
                    column_id = i
                if self.s.COL_COMMENT_NAME in cellval:
                    column_comment = i

                if config:
                    if self.s.COL_CONFIG_NAME in cellval:
                        column_config = i

                if eng_var:
                    if self.s.COL_ENG_UNIT_NAME in cellval:
                        column_eng_unit = i
                    if self.s.COL_ENG_MIN_NAME in cellval:
                        column_eng_min = i
                    if self.s.COL_ENG_MAX_NAME in cellval:
                        column_eng_max = i
        else:
            column_id = self.s.COL_ID
            column_comment = self.s.COL_COMMENT
            if config:
                column_config = self.s.COL_CONFIG
            if eng_var:
                column_eng_unit = self.s.COL_ENG_UNIT
                column_eng_min = self.s.COL_ENG_MIN
                column_eng_max = self.s.COL_ENG_MAX

        if self.s.debug_level > 0:
            print('SHEET:', sheet)
            print('\t', 'column_id:', column_id)
            print('\t', 'column_comment:', column_comment)
            if config:
                print('\t', 'column_config:', column_config)
            if eng_var:
                print('\t', 'column_eng_unit:', column_eng_unit)
                print('\t', 'column_eng_min:', column_eng_min)
                print('\t', 'column_eng_max:', column_eng_max)

        # Loop through object list and add key-value pairs to object dict
        # then append each object-dict to list
        obj_list = []
        idx = start_index
        for i in range(self.s.ROW, ws.max_row + 1):
            # Break if we get a blank ID cell
            cell_id = ws.cell(row=i, column=column_id)
            cell_comment = ws.cell(row=i, column=column_comment)
            if cell_id.value is None:
                break

            # Always insert these key-value pairs
            obj = {
                'type': type,
                'id': cell_id.value,
                'comment': cell_comment.value,
                'index': idx,
            }

            # Add conditional key-value pairs
            if config:
                cell_config = ws.cell(row=i, column=column_config)
                obj['config'] = cell_config.value

            if eng_var:
                cell_eng_unit = ws.cell(row=i, column=column_eng_unit)
                obj['eng_unit'] = cell_eng_unit.value
                cell_eng_min = ws.cell(row=i, column=column_eng_min)
                obj['eng_min'] = cell_eng_min.value
                cell_eng_max = ws.cell(row=i, column=column_eng_max)
                obj['eng_max'] = cell_eng_max.value

            obj_list.append(obj)
            idx += 1

        return obj_list

    def create_subdirs(self):
        """Create all subdirectiories beyond output path"""
        dirs = [self.s.TIA_DIR, self.s.INTOUCH_DIR]
        for dir in dirs:
            newdir = os.path.join(self.output_path, dir)
            if not os.path.exists(newdir):
                os.makedirs(newdir)

    def get_config_from_config_path(self):
        """Load config from .json file"""
        json_file = os.path.join(self.config_path, 'config_type.json')
        with open(json_file, 'r') as (f):
            json_var = json.load(f)
            self.config_type = json_var['type']
            print(f'Config Type={self.config_type}')

    @staticmethod
    def _print_disabled_in_settings(prefix):
        print(f"{prefix} not generated, disabled in settings file")

    def generate(self):
        print('Version', self.s.version)

        self.copy_excel_data_to_dictionaries()

        if self.s.debug_level > 0:
            for dict in self.dict_list:
                for obj in dict:
                    print(obj)

        self.get_config_from_config_path()
        self.create_subdirs()

        if self.s.VALVE_DISABLE:
            self._print_disabled_in_settings('Valve')
        else:
            Valve(self, self.output_path, self.valve_dict, self.config_path,
                  config_type=self.config_type)

        if self.s.MOTOR_DISABLE:
            self._print_disabled_in_settings('Motor')
        else:
            Motor(self, self.output_path, self.motor_dict, self.config_path,
                  config_type=self.config_type)

        if self.s.DI_DISABLE:
            self._print_disabled_in_settings('DI')
        else:
            DI(self, self.output_path, self.di_dict, self.config_path,
                config_type=self.config_type)

        if self.s.DO_DISABLE:
            self._print_disabled_in_settings('DO')
        else:
            DO(self, self.output_path, self.do_dict, self.config_path,
                config_type=self.config_type)
