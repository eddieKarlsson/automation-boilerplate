import sys
import os
from os import listdir
from os.path import isfile, join
import json
import openpyxl as xl
from settings import Settings
from obj_lib.valve import Valve
from obj_lib.motor import Motor
from obj_lib.di import DI
from obj_lib.do import DO
from obj_lib.ai import AI
from obj_lib.ao import AO
from obj_lib.pid import PID
from obj_lib.sum import SUM
from obj_lib.alarm import Alarm
from obj_lib.asi import ASi


class GenMain:
    """Main class called from UI,
    read data from excel and then execute sub-class functions
    """
    def __init__(self, excel_path, output_path, config_path):
        self.excel_path = excel_path
        self.output_path = output_path
        self.config_path = config_path        
        self.plcinexcel = set()
        self.s = Settings()
        self.dict_list = []
        self.it_path = os.path.join(self.output_path, self.s.INTOUCH_DIR)
        self.sql_path = os.path.join(self.output_path, self.s.SQL_DIR)

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
                        self.s.DI_SHEETNAME, self.s.DI_START_INDEX, 'di')
            self.dict_list.append(self.di_dict)

        if not self.s.DO_DISABLE:
            self.do_dict = self._obj_data_to_dict(
                        self.s.DO_SHEETNAME, self.s.DO_START_INDEX, 'do')
            self.dict_list.append(self.do_dict)

        if not self.s.VALVE_DISABLE:
            self.valve_dict = self._obj_data_to_dict(
                self.s.VALVE_SHEETNAME, self.s.VALVE_START_INDEX, 'valve', config=True)
            self.dict_list.append(self.valve_dict)

        if not self.s.MOTOR_DISABLE:
            self.motor_dict = self._obj_data_to_dict(
                self.s.MOTOR_SHEETNAME, self.s.MOTOR_START_INDEX, 'motor', config=True)
            self.dict_list.append(self.motor_dict)

        if not self.s.AI_DISABLE:
            self.ai_dict = self._obj_data_to_dict(
                self.s.AI_SHEETNAME, self.s.AI_START_INDEX, 'ai', eng_var=True)
            self.dict_list.append(self.ai_dict)

        if not self.s.AO_DISABLE:
            self.ao_dict = self._obj_data_to_dict(
                    self.s.AO_SHEETNAME, self.s.AO_START_INDEX, 'ao', eng_var=True)
            self.dict_list.append(self.ao_dict)

        if not self.s.PID_DISABLE:
            self.pid_dict = self._obj_data_to_dict(
                    self.s.PID_SHEETNAME, self.s.PID_START_INDEX, 'pid', eng_var=True)
            self.dict_list.append(self.pid_dict)

        if not self.s.SUM_DISABLE:
            self.sum_dict = self._obj_data_to_dict(
                    self.s.SUM_SHEETNAME, self.s.SUM_START_INDEX, 'sum', eng_var=True, volumeperpulse=True)
            self.dict_list.append(self.sum_dict)

        if not self.s.ALARM_DISABLE:
            self.alarm_dict = self._obj_data_to_dict(
                    self.s.ALARM_SHEETNAME, self.s.ALARM_START_INDEX, 'alarm', generic_alarm=True)
            self.dict_list.append(self.alarm_dict)

        if not self.s.ASI_DISABLE:
            self.asi_dict = self._obj_data_to_dict(
                    self.s.ASI_SHEETNAME, self.s.ASI_START_INDEX, 'asi', asi=True)
            self.dict_list.append(self.asi_dict)

    def _obj_data_to_dict(self, sheet, start_index, type, config=False, eng_var=False, volumeperpulse=False,
                          generic_alarm=False, asi=False):
        """Read all object data to dict"""

        # Open excel sheet
        try:
            ws = self.wb[sheet]
        except KeyError:
            msg = f'ERROR! {sheet} sheet does not exist, program will exit'
            print(msg)
            sys.exit()

            # Loop header and set the corresponding variables to
            # the integer number
        for i in range(1, 20):
            cell = ws.cell(row=self.s.HEADER_ROW, column=i)
            cellval = str(cell.value)

            # If cell is empty (NoneType) - skip it
            if cellval is None:
                continue

            if self.s.COL_ID_NAME == cellval:
                column_id = i
            if self.s.COL_COMMENT_NAME == cellval:
                column_comment = i
            if self.s.COL_ALARM_GROUP_NAME == cellval:
                column_alarmgroup = i
            if self.s.COL_PLC_NAME == cellval:
                column_plc = i

            if config:
                if self.s.COL_CONFIG_NAME == cellval:
                    column_config = i

            if volumeperpulse:
                if self.s.COL_VolumePerPulse_Name == cellval:
                    column_volumeperpulse = i

            if eng_var:
                if self.s.COL_ENG_UNIT_NAME == cellval:
                    column_eng_unit = i
                if self.s.COL_ENG_MIN_NAME == cellval:
                    column_eng_min = i
                if self.s.COL_ENG_MAX_NAME == cellval:
                    column_eng_max = i

            if generic_alarm:
                if self.s.COL_ALARM_PRIO_NAME == cellval:
                    column_alarm_prio = i
                if self.s.COL_ALARM_TEXT_NAME == cellval:
                    column_alarm_text = i

            if asi:
                if self.s.COL_ASI_ADDR_NAME == cellval:
                    column_asi_addr = i
                if self.s.COL_ASI_MASTER_NAME == cellval:
                    column_asi_master = i

        if self.s.debug_level > 0:
            print('SHEET:', sheet)
            print('\t', 'column_id:', column_id)
            print('\t', 'column_comment:', column_comment)
            print('\t', 'column_alarmgroup:', column_alarmgroup)
            print('\t', 'column_plc:', column_plc)
            if config:
                print('\t', 'column_config:', column_config)
            if volumeperpulse:
                print('\t', 'column_volumeperpulse:', column_volumeperpulse)
            if eng_var:
                print('\t', 'column_eng_unit:', column_eng_unit)
                print('\t', 'column_eng_min:', column_eng_min)
                print('\t', 'column_eng_max:', column_eng_max)
            if generic_alarm:
                print('\t', 'column_alarm_prio:', column_alarm_prio)
                print('\t', 'column_alarm_text:', column_alarm_text)
            if asi:
                print('\t', 'column_asi_addr:', column_asi_addr)
                print('\t', 'column_asi_master:', column_asi_master)


        # Loop through object list and add key-value pairs to object dict
        # then append each object-dict to list
        obj_list = []
        index = start_index
        for i in range(self.s.ROW, ws.max_row + 1):
            # Break if we get a blank ID cell
            cell_id = ws.cell(row=i, column=column_id)
            cell_comment = ws.cell(row=i, column=column_comment)
            cell_alarmgroup = ws.cell(row=i, column=column_alarmgroup)
            cell_plc = ws.cell(row=i, column=column_plc)

            if cell_id.value is None:
                break

            # Always insert these key-value pairs
            obj = {
                'type': type,
                'id': cell_id.value,
                'comment': cell_comment.value,
                'index': index,
                'alarmgroup': cell_alarmgroup.value,
                'plc': cell_plc.value,
            }

            # Add conditional key-value pairs
            if config:
                cell_config = ws.cell(row=i, column=column_config)
                obj['config'] = cell_config.value

            if volumeperpulse:
                cell_volumeperpulse = ws.cell(row=i, column=column_volumeperpulse)
                obj['volumeperpulse'] = cell_volumeperpulse.value

            if eng_var:
                cell_eng_unit = ws.cell(row=i, column=column_eng_unit)
                obj['eng_unit'] = cell_eng_unit.value
                cell_eng_min = ws.cell(row=i, column=column_eng_min)
                obj['eng_min'] = cell_eng_min.value
                cell_eng_max = ws.cell(row=i, column=column_eng_max)
                obj['eng_max'] = cell_eng_max.value

            if generic_alarm:
                cell_alarm_text = ws.cell(row=i, column=column_alarm_text)
                obj['alarm_text'] = cell_alarm_text.value
                cell_alarm_prio = ws.cell(row=i, column=column_alarm_prio)
                obj['alarm_prio'] = cell_alarm_prio.value

            if asi:
                cell_asi_addr = ws.cell(row=i, column=column_asi_addr)
                obj['asi_addr'] = cell_asi_addr.value
                cell_asi_master = ws.cell(row=i, column=column_asi_master)
                obj['asi_master'] = cell_asi_master.value

            obj_list.append(obj)
            index += 1

        for obj in obj_list:
            self.plcinexcel.add(obj['plc'])

        return obj_list

    def create_subdirs(self):
        """Create all subdirectiories beyond output path"""
        dirs = [self.s.TIA_DIR, self.s.INTOUCH_DIR, self.s.SQL_DIR]
        for dir in dirs:
            newdir = os.path.join(self.output_path, dir)
            if not os.path.exists(newdir):
                os.makedirs(newdir)

    def create_subdirsplc(self):
        """Create all subdirectiories beyond output path"""
        for plc in self.plcinexcel:
            newdir = os.path.join(self.output_path, self.s.TIA_DIR)
            newdir = os.path.join(newdir, plc)
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

    def _combine_it_files(self):
        """
        combines all it files in folder and chops off first lines
        in files other than the first
        """

        outfile = os.path.join(self.it_path, "ALL_IT.csv")

        if os.path.exists(outfile):
            os.remove(outfile)

        file_list = [f for f in listdir(self.it_path)
                     if isfile(join(self.it_path, f))]

        with open(outfile, 'w', encoding='cp1252') as wf:
            for file_index, file in enumerate(file_list):
                with open(os.path.join(self.it_path, file), 'r', encoding='cp1252') as rf:
                    for line_index, line in enumerate(rf):
                        # Skip first line header if it's not the first file
                        if file_index > 0 and line_index <= 0:
                            continue
                        wf.write(line)

    def _combine_sql_files(self):
        """
        combines all it files in folder and chops off first lines
        in files other than the first
        """

        outfile = os.path.join(self.sql_path, "ALL_SQL.csv")

        if os.path.exists(outfile):
            os.remove(outfile)

        file_list = [f for f in listdir(self.sql_path)
                     if isfile(join(self.sql_path, f))]

        with open(outfile, 'w', encoding='cp1252') as wf:
            for file_index, file in enumerate(file_list):
                with open(os.path.join(self.sql_path, file), 'r', encoding='cp1252') as rf:
                    for line_index, line in enumerate(rf):
                        wf.write(line)

    def generate(self):
        print('Version', self.s.version)

        self.copy_excel_data_to_dictionaries()

        if self.s.debug_level > 0:
            for dict in self.dict_list:
                for obj in dict:
                    print(obj)

        self.get_config_from_config_path()
        self.create_subdirs()
        self.create_subdirsplc()

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

        if self.s.AI_DISABLE:
            self._print_disabled_in_settings('AI')
        else:
            AI(self, self.output_path, self.ai_dict, self.config_path,
                config_type=self.config_type)

        if self.s.AO_DISABLE:
            self._print_disabled_in_settings('AO')
        else:
            AO(self, self.output_path, self.ao_dict, self.config_path,
                config_type=self.config_type)

        if self.s.PID_DISABLE:
            self._print_disabled_in_settings('PID')
        else:
            PID(self, self.output_path, self.pid_dict, self.config_path,
                config_type=self.config_type)

        if self.s.SUM_DISABLE:
            self._print_disabled_in_settings('SUM')
        else:
            SUM(self, self.output_path, self.sum_dict, self.config_path,
                config_type=self.config_type)

        if self.s.ALARM_DISABLE:
            self._print_disabled_in_settings('Alarm')
        else:
            Alarm(self, self.output_path, self.alarm_dict, self.config_path,
                config_type=self.config_type)

        if self.s.ASI_DISABLE:
            self._print_disabled_in_settings('ASi')
        else:
            ASi(self, self.output_path, self.asi_dict, self.config_path, config_type=self.config_type)

        self._combine_it_files()
        self._combine_sql_files()
