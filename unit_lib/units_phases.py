import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


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

    def _intouch_file(self):
        #  TODO all
        data = self.gen.single(self.cf, self.rl, 'Intouch_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'Intouch_Tag')

        filename = self.type + '_it.csv'
        path = os.path.join(self.it_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _intouch(self):

        for obj in self.ol:
            obj_id = obj['id']
            obj_type = obj['type']
            obj_plc = obj['plc']

            #  Skip object if not valid
            if not obj['is_valid_unit_type']:
                print(f'\nWARNING: ID {obj_id} is skipped, invalid Type')
                continue

            if obj['is_unit']:
                #  TODO create path to unit subfolder
                #  TODO append the new folder to a list of folders of all units
                #  TODO Create Intouch file to subfolder

                pass
            elif obj['is_phase']:
                #  TODO Create Intouch file to subfolder

                pass


            

            
            


    def generate(self):
        for obj in self.ol:
            print(obj)
        pass
