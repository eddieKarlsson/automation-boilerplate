import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class DI:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path,
                 config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'di'
        self.config_type = config_type

        self.cp = os.path.join(config_path, self.type)  # Config folder path
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.tia_path = os.path.join(self.output_path, self.s.TIA_DIR)
        self.it_path = os.path.join(self.output_path, self.s.INTOUCH_DIR)
        self.sql_path = os.path.join(self.output_path, self.s.SQL_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(f'\nWARNING: {self.type.upper()} not generated, no items found in TD')


    def _tia_db(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

        filename = self.type + '_db.db'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_symbol(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl,
                                 'TIA_Symbol')

        filename = self.type + '_symbols.sdf'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_code(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_Code_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_Code_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_Code_Constant')
        data += self.gen.multiple(self.ol, self.cf, self.rl,
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

    def _sql(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'SQLProcedure')

        filename = self.type + '_sql.csv'
        path = os.path.join(self.sql_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def generate(self):
        """Callup"""
        if self.config_type == 'mc':
            self._tia_db()
            self._tia_symbol()
            self._tia_code()
            self._intouch()
            self._sql()
            self.gen.result(self.rl, type=self.type.upper())
