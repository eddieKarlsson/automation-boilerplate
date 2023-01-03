import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class ASi:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path, config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'asi'
        self.masterfolder = 'HW'
        self.config_type = config_type

        self.cp = os.path.join(config_path, self.masterfolder, self.type)  # Config folder path
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.tia_path = os.path.join(self.output_path, self.masterfolder, self.s.TIA_DIR)
        self.it_path = os.path.join(self.output_path, self.masterfolder, self.s.INTOUCH_DIR)
        self.sql_path = os.path.join(self.output_path, self.masterfolder, self.s.SQL_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(f'\nWARNING: {self.type.upper()} not generated, no items found in TD')

    def _tia_code(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_FB_HEADER')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_FB_INOUT')
        data += self.gen.single(self.cf, self.rl, 'TIA_FB_BEGIN')
        data += self.gen.single(self.cf, self.rl, 'TIA_FB_CODE1')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_FB_CODE2')
        data += self.gen.single(self.cf, self.rl, 'TIA_FB_CODE3')

        filename = self.type + '_code.scl'
        pathwithplc = path = os.path.join(self.tia_path, self.plc)
        path = os.path.join(pathwithplc, filename)
        if not os.path.exists(pathwithplc):
            os.makedirs(pathwithplc)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_code_multiple_plc(self):
        for plc in self.plc_set:
            for asmaster in self.asimaster_set:
                if asmaster:
                    for same in self.asmasterinplc_set:
                        if (plc+':'+asmaster) == same:
                            data = self.gen.single_withreplace(self.cf, self.rl, 'TIA_FB_HEADER', self.s.ASI_MASTER_REPLACE, asmaster)
                            data += self.gen.multiple_twochecks(self.ol, self.cf, self.rl, 'TIA_FB_INOUT', plc, asmaster)
                            data += self.gen.single(self.cf, self.rl, 'TIA_FB_BEGIN')
                            data += self.gen.single(self.cf, self.rl, 'TIA_FB_CODE1')
                            data += self.gen.multiple_twochecks(self.ol, self.cf, self.rl, 'TIA_FB_CODE2', plc, asmaster)
                            data += self.gen.single(self.cf, self.rl, 'TIA_FB_CODE3')

                            filename = plc + '_' + asmaster + '_' + self.type + '_code.scl'
                            pathwithplc = path = os.path.join(self.tia_path, plc)
                            path = os.path.join(pathwithplc, filename)
                            if not os.path.exists(pathwithplc):
                                os.makedirs(pathwithplc)
                            with open(path, 'w', encoding='cp1252') as f:
                                f.write(data)


    def _find_plcs(self):
        """find what plcs are in the object list"""
        self.plc_set = set()  # Create a set,  doesnt allow duplicate values
        for obj in self.ol:
            self.plc_set.add(obj['plc'])

    def _find_asmasterinplc_set(self):
        self.asmasterinplc_set = set()
        for obj in self.ol:
            if obj['asi_master']:
                self.asmasterinplc_set.add(obj['plc']+':'+obj['asi_master'])


    def _find_asimasters_set(self):
        """find what asi masters are in the object list"""
        self.asimaster_set = set()  # Create a set,  doesnt allow duplicate values
        for obj in self.ol:
            self.asimaster_set.add(obj['asi_master'])

    def generate(self):
        if self.ol:
            self._find_plcs()
            self._find_asimasters_set()
            self._find_asmasterinplc_set()
            self._tia_code_multiple_plc()
            self.gen.result(self.rl, type=self.type.upper())
