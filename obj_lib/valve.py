import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class Valve:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path, config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'valve'
        self.masterfolder = 'CMs'
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

    def _tia_db(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_DB_Begin')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Parameters')
        data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

        filename = self.type + '_db.db'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _find_plcs(self):
        """find what plcs are in the object list"""
        self.plc_set = set()  # Create a set,  doesnt allow duplicate values
        for obj in self.ol:
            self.plc_set.add(obj['plc'])

    def _tia_db_multiple_plc(self):
        for plc in self.plc_set:
            data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
            data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var', plc_name=plc)
            data += self.gen.single(self.cf, self.rl, 'TIA_DB_Begin')
            data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Parameters', plc_name=plc)
            data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

            filename = plc + '_' + self.type + '_db.db'
            pathwithplc = os.path.join(self.tia_path, plc)
            path = os.path.join(pathwithplc, filename)
            if not os.path.exists(pathwithplc):
                os.makedirs(pathwithplc)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _tia_tag(self):
            all_attr = self.get_all_config_attributes()

            for plc in self.plc_set:
                data = ''
                for obj in self.ol:
                    if obj['plc'] != plc:
                        continue

                    for attr in all_attr:
                        if obj.get(attr) is not None:
                            ref_txt = 'TIA_tag_' + attr
                            data += self.gen.single_replace(self.cf, self.rl, ref_txt, obj, 
                                                            replace='@' + ref_txt, replace_with=obj[attr])
                            
                filename = plc + '_' + self.type + '_plctags.sdf'
                outdir = path = os.path.join(self.tia_path, plc, 'tags', 'subfiles')
                path = os.path.join(outdir, filename)
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                with open(path, 'w', encoding='cp1252') as f:
                    f.write(data)

    def _tia_iocopy(self):
            all_attr = self.get_all_config_attributes()

            for plc in self.plc_set:
                data = ''
                for obj in self.ol:
                    if obj['plc'] != plc:
                        continue
                    
                    for attr in all_attr:
                        if obj.get(attr) is not None:
                            ref_txt = 'TIA_IOcopy_' + attr
                            data += self.gen.single_replace(self.cf, self.rl, ref_txt, obj, 
                                                            replace=ref_txt, replace_with=obj[attr])
                    data += '\n'    # to separate objects
                            
                filename = plc + '_' + self.type + '_iocopy.scl'
                outdir = path = os.path.join(self.tia_path, plc, 'iocopy', 'subfiles')
                path = os.path.join(outdir, filename)
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                with open(path, 'w', encoding='cp1252') as f:
                    f.write(data)

    def _tia_code(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_Code_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_Code_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_Code_Var_Footer')
        data += self.gen.multiple_config(self.ol, self.cp, self.rl, 'TIA_Code_Body')
        data += self.gen.single(self.cf, self.rl, 'TIA_Code_Footer')

        filename = self.type + '_code.awl'
        path = os.path.join(self.tia_path, filename)
        if not os.path.exists(self.tia_path):
            os.makedirs(self.tia_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _intouch(self):
        data = self.gen.single(self.cf, self.rl, 'Intouch_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'Intouch_Tag')

        filename = self.type + '_IT.csv'
        path = os.path.join(self.it_path, filename)
        if not os.path.exists(self.it_path):
            os.makedirs(self.it_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _sql(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'SQLProcedure')

        filename = self.type + '_sql.csv'
        path = os.path.join(self.sql_path, filename)
        if not os.path.exists(self.sql_path):
            os.makedirs(self.sql_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def generate(self):
        if self.ol:
            self._find_plcs()
            self._tia_db_multiple_plc()
            self._tia_tag()
            self._tia_iocopy()
            #self._tia_code()
            self._intouch()
            self._sql()
            self.gen.result(self.rl, type=self.type.upper())

    @staticmethod
    def decode_config_attributes(config):
        """ 
        Decode the configuration word and returns a list of attributes in string format
        TIA Config:
            #VLV.Config.Main': = #VLV.Config.UI_Config.%X0;
            #VLV.Config.Upper': = #VLV.Config.UI_Config.%X1;
            #VLV.Config.Lower': = #VLV.Config.UI_Config.%X2;
            #VLV.Config."Main Active FB"': = #VLV.Config.UI_Config.%X3;
            #VLV.Config."Main DeActive FB"': = #VLV.Config.UI_Config.%X4;
        """
        attributes = []

        val = int(config)

        if val & 0b1:
            attributes.append('main_act')    
        if val & 0b10:
            attributes.append('upperseat_act')    
        if val & 0b100:
            attributes.append('lowerseat_act')
        if val & 0b1000:
            attributes.append('main_act_fb')
        if val & 0b10000:
            attributes.append('main_deact_fb')

        # If list is empty return None
        if attributes:
            return attributes
        else:
            return None

    def get_all_config_attributes(self):
        # Returns a list of all tag attributes
        return self.decode_config_attributes(0xFFFF)
