import os
import os.path
from gen_unit_func import GenUnitFunc as genfunc
from os import listdir
from os.path import isfile, join



class UnitsPhases:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path, config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'Units_Phases'
        self.config_type = config_type

        self.cp = os.path.join(config_path, self.type)  # Config folder path

        self.output_path = output_path
        self.it_path = os.path.join(self.output_path, self.s.INTOUCH_DIR, self.type)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"
        
        self.it_all_all_path_list = []

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(f'\nWARNING: {self.type.upper()} not generated, no items found in TD')


    def intouch(self):

        for obj in self.ol:
            # unpack dict object to var
            obj_id = obj['id']
            obj_is_valid_unit_type = obj['is_valid_unit_type']
            obj_is_unit = obj['is_unit']
            obj_is_phase = obj['is_phase']
            obj_parent = obj['parent']

            #  Skip object if not valid
            if not obj_is_valid_unit_type:
                if obj_parent is None:
                    self.gen.append_bad_result(f'WARNING: {obj_id} is skipped, invalid Type',
                                                self.rl)
                else:
                    self.gen.append_bad_result(f'{obj_parent}_{obj_id} is skipped, invalid Type',
                                                self.rl)
                continue

            #  Control logic if object is valid
            if obj_is_unit:
                dest_dir = os.path.join(self.it_path, obj_id)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                self._create_intouch_file(dest_dir, obj)
            elif obj_is_phase:
                # Check if parent dir of unit exists, if not skip the object
                if not os.path.exists(dest_dir):
                    self.gen.append_bad_result(f'\nWARNING: {obj_parent}{obj_id} skipped, expected this dir {dest_dir} but not found!')
                    continue
                self._create_intouch_file(dest_dir, obj)
                


    def _create_intouch_file(self, path, obj):
        """Creates intouch file and adds path to file to dictionary"""
        config_file = os.path.join(self.cp, obj['type'] + '.txt')
        data = self.gen.single_obj(config_file, self.rl, obj, obj['type'] + '_IT')

        if obj['parent'] is None:
            filename = obj['id'] + '_IT.csv'
        else:
            filename = obj['parent']+ '_' + obj['id'] + '_IT.csv'
        path = os.path.join(path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)
        
        if obj['parent'] is None and obj['is_unit']:
            obj['it_file_path'] = path  #Create new property, intouch file path


    def combine_intouch_files_same_unit(self):
        """Combines intouch files and writes a "ALL" file to the group folder"""
        for obj in self.ol:
            if obj['parent'] is None and obj['is_unit']:
                folder_path, fname = os.path.split(obj['it_file_path'])
                all_filename = f"ALL_{obj['id']}.csv"
                all_path = os.path.join(folder_path, all_filename)
            
                if os.path.exists(all_path):
                    os.remove(all_path)

                file_list = [f for f in listdir(folder_path)
                    if isfile(join(folder_path, f))]

                with open(all_path, 'w', encoding='cp1252') as wf:
                    for file_index, file in enumerate(file_list):
                        with open(os.path.join(folder_path, file), 'r', encoding='cp1252') as rf:
                            for line_index, line in enumerate(rf):
                                # Skip first line header if it's not the first file
                                if file_index > 0 and line_index <= 0:
                                    continue
                                wf.write(line)
                self.it_all_all_path_list.append(all_path)


    def combine_intouch_all_all_files(self):
        """Combines intouch files and writes a "ALL" file to the group folder"""
        all_filename = f"ALL_{self.type.upper()}_IT.csv"
        all_path = os.path.join(self.it_path, all_filename)
            
        with open(all_path, 'w', encoding='cp1252') as wf:
            for file_index, file in enumerate(self.it_all_all_path_list):
                with open(file, 'r', encoding='cp1252') as rf:
                    for line_index, line in enumerate(rf):
                        # Skip first line header if it's not the first file
                        if file_index > 0 and line_index <= 0:
                            continue
                        wf.write(line)
         



    def generate(self):
        self.intouch()
        self.gen.result(self.rl, type=self.type.upper())
        self.combine_intouch_files_same_unit()
        self.combine_intouch_all_all_files()
