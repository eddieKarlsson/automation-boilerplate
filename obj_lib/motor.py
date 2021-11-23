import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class Motor:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path,
                 config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'motor'
        self.config_type = config_type

        self.cp = os.path.join(config_path, self.type)  # Config folder path
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.tia_path = os.path.join(self.output_path, self.s.TIA_DIR)
        self.it_path = os.path.join(self.output_path, self.s.INTOUCH_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        self.generate()

    def _tia_db(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

        filename = self.type + '_db.db'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_symbol(self):
        data = self.gen.multiple_config(self.ol, self.cp, self.rl,
                                        'TIA_Symbol')

        filename = self.type + '_symbols.sdf'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_code(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_Code_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_Code_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_Code_Var_Footer')
        data += self.gen.multiple_config(self.ol, self.cp, self.rl,
                                         'TIA_Code_Body')
        data += self.gen.single(self.cf, self.rl, 'TIA_Code_Footer')

        filename = self.type + '_code.awl'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _intouch(self):
        data = self.gen.single(self.cf, self.rl, 'Intouch_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'Intouch_Tag')

        filename = self.type + '_it.csv'
        path = os.path.join(self.it_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def generate(self):
        """Callup"""
        if self.config_type == 'mc':
            self._tia_db()
            self._tia_symbol()
            self._tia_code()
            self._intouch()
            self.gen.result(self.rl, type=self.type.upper())
