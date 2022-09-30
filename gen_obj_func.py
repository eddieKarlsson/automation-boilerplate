import os
import os.path


class GenObjFunc:
    """Multiple functions to interact with worbook and sub-classes in obj_lib,
    and ui.
    """
    def __init__(self, gen_main):
        self.s = gen_main.s

    def _replace_keywords(self, line, obj):
        """Take in a line and convert all the identifiers to obj data"""

        # Replace the keywords that always exists
        line = line.replace(self.s.ID_REPLACE, obj['id'])
        line = line.replace(self.s.ALARM_GROUP_REPLACE, obj['alarmgroup'])
        line = line.replace("@Type", obj['type'])

        # check if comment exists, if not insert empty string
        if obj['comment'] is None:
            line = line.replace(self.s.COMMENT_REPLACE, '')
        else:
            line = line.replace(self.s.COMMENT_REPLACE,
                                obj['comment'])

        # Replace index
        line = line.replace(self.s.INDEX_REPLACE, str(obj['index']))

        # Replace PLC
        if obj['plc'] is None:
            line = line.replace(self.s.PLC_REPLACE, '')
        else:
            line = line.replace(self.s.PLC_REPLACE,
                                obj['plc'])

        # Replace the keywords that are optional (check if they exist)
        if obj.get('config') is not None:
            line = line.replace(self.s.CONFIG_REPLACE, str(obj['config']))

        if obj.get('volumeperpulse') is not None:
            line = line.replace(self.s.VolumePerPulse_REPLACE, str(obj['volumeperpulse']))

        if obj.get('eng_unit') is not None:
            line = line.replace(self.s.ENG_UNIT_REPLACE,
                                obj['eng_unit'])
        else:
            line = line.replace(self.s.ENG_UNIT_REPLACE, '')

        if obj.get('eng_min') is not None:
            line = str(line.replace(self.s.ENG_MIN_REPLACE,
                                    str(obj['eng_min'])))
        else:
            line = line.replace(self.s.ENG_MIN_REPLACE, '0')

        if obj.get('eng_max') is not None:
            line = str(line.replace(self.s.ENG_MAX_REPLACE,
                                    str(obj['eng_max'])))
        else:
            line = line.replace(self.s.ENG_MAX_REPLACE, '100')

        if obj.get('alarm_text') is not None:
            line = line.replace(self.s.ALARM_TEXT_REPLACE, obj['alarm_text'])

        if obj.get('alarm_prio') is not None:
            line = line.replace(self.s.ALARM_PRIO_REPLACE, str(obj['alarm_prio']))

        if obj.get('asi_addr') is not None:
            line = line.replace(self.s.ASI_ADDR_REPLACE, str(obj['asi_addr']))     

        if obj.get('asi_master') is not None:
            line = line.replace(self.s.ASI_MASTER_REPLACE, str(obj['asi_master']))   

        return line

    @staticmethod
    def single(config_file, list_result, ref_txt):
        """Read a text file and copy the data inside notifiers to memory"""
        with open(config_file, 'r') as config:
            exists_in_config = False
            section_found = False
            inst_data = ''
            begin = '<' + ref_txt + '>'
            end = '</' + ref_txt + '>'

            for line in config:
                if end in str(line):
                    section_found = False
                if section_found:                    
                    inst_data += line
                if begin in str(line):
                    exists_in_config = True
                    section_found = True
        if not exists_in_config:
            result_ok = False
            result_msg = f"'{ref_txt}' not found in config file"
        else:
            result_ok = True
            result_msg = None

        # Return a dictionary with the result
        result = {
            'ref_txt': ref_txt,
            'type': None,
            'result_ok': result_ok,
            'bad_result_msg': result_msg
        }

        list_result.append(result)
        return inst_data

    def multiple(self, obj_list, config_file, list_result, ref_txt, plc_name=None):
        """Get text lines from config file and replace by data in excel for
            each item, then append the new lines to memory"""

        with open(config_file, 'r') as config:
            exists_in_config = False
            section_found = False
            inst_data = ''
            begin = '<' + ref_txt + '>'
            end = '</' + ref_txt + '>'

            for obj in obj_list:
                if plc_name is not None and plc_name != obj['plc']:
                    continue            

                config.seek(0, 0)  # Seek to beginning of file
                for line_index, line in enumerate(config, start=1):
                    if end in str(line):
                        section_found = False
                    if section_found:
                        line = self._replace_keywords(line, obj)
                        inst_data += line
                    if begin in str(line):
                        exists_in_config = True
                        section_found = True

            if not exists_in_config:
                result_ok = False
                result_msg = f"'{ref_txt}' not found in config file"
            else:
                result_ok = True
                result_msg = None

            # Return a dictionary with the result
            result = {
                'ref_txt': ref_txt,
                'type': None,
                'result_ok': result_ok,
                'bad_result_msg': result_msg
            }

        list_result.append(result)
        return inst_data

    def multiple_config(self, obj_list, sub_dir, list_result, ref_txt,
                        data_size=30, data_offset=14):
        """Same as td_multiple, but config stored in different files"""
        # Setup variables
        exists_in_config = False
        section_found = False
        inst_data = ''
        begin = '<' + ref_txt + '>'
        end = '</' + ref_txt + '>'

        # loop through excel rows, get value at corresponding cell
        for obj in obj_list:
            # combine file path and open corresponding file
            filename = obj['config'] + '.txt'
            file_and_path = os.path.join(sub_dir, filename)

            with open(file_and_path, 'r') as config:
                for line_index, line in enumerate(config, start=1):
                    if end in str(line):
                        section_found = False
                    if section_found:
                        line = self._replace_keywords(line, obj, data_size, data_offset)
                        inst_data += line
                    if begin in str(line):
                        exists_in_config = True
                        section_found = True

                    # will be last item processed but doesn't matter
                    type = obj['type']
            if not exists_in_config:
                result_ok = False
                result_msg = f"'{ref_txt}' not found in config file"
            else:
                result_ok = True
                result_msg = None

            # Return a dictionary with the result
            result = {
                'ref_txt': ref_txt,
                'type': None,
                'result_ok': result_ok,
                'bad_result_msg': result_msg
            }
        list_result.append(result)
        return inst_data

    @staticmethod
    def single_withreplace(config_file, list_result, ref_txt, replace, obj):
        """Read a text file and copy the data inside notifiers to memory"""
        with open(config_file, 'r') as config:
            exists_in_config = False
            section_found = False
            inst_data = ''
            begin = '<' + ref_txt + '>'
            end = '</' + ref_txt + '>'

            for line in config:
                if end in str(line):
                    section_found = False
                if section_found:        
                    line = line.replace(replace, obj)             
                    inst_data += line
                if begin in str(line):
                    exists_in_config = True
                    section_found = True
        if not exists_in_config:
            result_ok = False
            result_msg = f"'{ref_txt}' not found in config file"
        else:
            result_ok = True
            result_msg = None

        # Return a dictionary with the result
        result = {
            'ref_txt': ref_txt,
            'type': None,
            'result_ok': result_ok,
            'bad_result_msg': result_msg
        }

        list_result.append(result)
        return inst_data

    def multiple_twochecks(self, obj_list, config_file, list_result, ref_txt, plc_name=None, asmaster_name=None):
        """Get text lines from config file and replace by data in excel for
            each item, then append the new lines to memory"""

        with open(config_file, 'r') as config:
            exists_in_config = False
            section_found = False
            inst_data = ''
            begin = '<' + ref_txt + '>'
            end = '</' + ref_txt + '>'

            for obj in obj_list:
                if (plc_name is not None and plc_name != obj['plc']) or (asmaster_name is not None and asmaster_name != obj['asi_master']):
                    continue            

                config.seek(0, 0)  # Seek to beginning of file
                for line_index, line in enumerate(config, start=1):
                    if end in str(line):
                        section_found = False
                    if section_found:
                        line = self._replace_keywords(line, obj)
                        inst_data += line
                    if begin in str(line):
                        exists_in_config = True
                        section_found = True

                    # will be last item processed but doesn't matter
                    type = obj['type']
            if not exists_in_config:
                result_ok = False
                result_msg = f"'{ref_txt}' not found in config file"
            else:
                result_ok = True
                result_msg = None

            # Return a dictionary with the result
            result = {
                'ref_txt': ref_txt,
                'type': None,
                'result_ok': result_ok,
                'bad_result_msg': result_msg
            }

        list_result.append(result)
        return inst_data

    @staticmethod
    def result(list_with_dicts, type='undefined'):
        """Check all result dicts and sum them, then print info to user"""
        result_ok_cnt = 0
        result_bad_cnt = 0
        print('\n')
        print(type)

        good_results = []  # Empty list
        bad_results = []  # Empty list

        for dict in list_with_dicts:
            if dict['result_ok']:
                good_results.append(dict['ref_txt'])
                result_ok_cnt += 1
            else:
                msg = f"\t ERROR: {dict['bad_result_msg']}"
                bad_results.append(msg)
                result_bad_cnt += 1
        if result_ok_cnt > 0:
            tmp_text = "Succesfully processed"
            print(f"\t {tmp_text} {result_ok_cnt} objects: {good_results}")

        if result_bad_cnt > 0:
            print("\n")
            print(f"\t {result_bad_cnt} resulted with error:")
            for r in bad_results:
                print('\t', r)

        if result_ok_cnt == 0 and result_bad_cnt == 0:
            print("\t Nothing processed")
