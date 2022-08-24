import os
import os.path
from gen_unit_func import GenUnitFunc as genfunc


class UnitsPhases:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path, config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'Units_Phases'
        self.config_type = config_type

        self.cp = os.path.join(config_path, self.type)  # Config folder path

        self.output_path = output_path
        self.it_path = os.path.join(self.output_path, self.s.INTOUCH_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

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
                    print(f'\nWARNING: ID {obj_parent}_{obj_id} is skipped, invalid Type')
                else:
                    print(f'\nWARNING: ID {obj_id} is skipped, invalid Type')
            continue

            print('yo')
            if obj_is_unit:
                dest_dir = os.path.join(self.output_path, obj_id)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                self._create_intouch_file(dest_dir, obj)
            elif obj_is_phase:
                # Check if parent dir of unit exists, if not skip the object
                if not os.path.exists(dest_dir):
                    print(f'\nWARNING: {obj_parent}{obj_id} skipped, expected this dir but not found! {dest_dir}')
                    continue
                self._create_intouch_file(dest_dir, obj)
                


    def _create_intouch_file(self, path, obj):
        config_file = os.path.join(self.cp, obj['type'] + '.txt')
        data = self.gen.single_obj(config_file, self.rl, obj, obj['type'] + '_IT')

        if obj['parent'] is None:
            filename = obj['id'] + '_IT.csv'
        else:
            filename = obj['parent'] + obj['id'] + '_IT.csv'
        path = os.path.join(path, filename)
        with open(path, 'w') as f:
            f.write(data)


    def generate(self):
        self.intouch()