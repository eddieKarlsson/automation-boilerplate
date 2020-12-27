import os
import os.path


class GenObjFunc:
    """Multiple functions to interact with worbook and sub-classes in obj_lib,
    and ui.
    """
    def __init__(self, gen_main):
        self.s = gen_main.s

    def _replace_keywords(self, line, obj, data_size, data_offset):
        """Take in a line and convert all the identifiers to obj data"""

        # Replace the keywords that always exists
        line = line.replace(self.s.ID_REPLACE, obj['id'])

        # check if comment exists, if not insert empty string
        if obj['comment'] is None:
            line = line.replace(self.s.COMMENT_REPLACE, '')
        else:
            line = line.replace(self.s.COMMENT_REPLACE,
                                obj['comment'])

        # Replace index
        line = line.replace(self.s.INDEX_REPLACE, str(obj['index']))

        # calculate address by offset & datatype data_size
        adress = (obj['index'] * data_size) + data_offset
        # Replace '@ADR'
        line = line.replace(self.s.ADR_REPLACE, str(adress))

        # Replace PLC
        line = line.replace(self.s.PLC_REPLACE,
                            self.s.PLC_NAME)

        # Replace the keywords that are optional (check if they exist)

        if obj.get('config') is not None:
            line = line.replace(self.s.CONFIG_REPLACE, obj['config'])

        if obj.get('eng_unit') is not None:
            line = line.replace(self.s.ENG_UNIT_REPLACE,
                                obj['eng_unit'])
        else:
            line = line.replace(self.s.ENG_UNIT_REPLACE, '')

        if obj.get('eng_min') is not None:
            line = str(line.replace(self.s.ENG_MIN_REPLACE,
                                    obj['eng_min']))
        else:
            line = line.replace(self.s.ENG_MIN_REPLACE, '0')

        if obj.get('eng_max') is not None:
            line = str(line.replace(self.s.ENG_MAX_REPLACE,
                                    obj['eng_max']))
        else:
            line = line.replace(self.s.ENG_MAX_REPLACE, '100')

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
            resultOk = False
            resultMsg = f"'{ref_txt}' not found in config file"
        else:
            resultOk = True
            resultMsg = None

        # Return a dictionary with the result
        result = {
            'ref_txt': ref_txt,
            'type': None,
            'resultOk': resultOk,
            'badResultMsg': resultMsg
        }

        list_result.append(result)
        return inst_data

    def multiple(self, obj_list, config_file, list_result, ref_txt,
                 data_size=30, data_offset=14):
        """Get text lines from config file and replace by data in excel for
            each item, then append the new lines to memory"""

        with open(config_file, 'r') as config:
            exists_in_config = False
            section_found = False
            inst_data = ''
            begin = '<' + ref_txt + '>'
            end = '</' + ref_txt + '>'

            for obj in obj_list:
                config.seek(0, 0)  # Seek to beginning of file
                for lineIndex, line in enumerate(config, start=1):
                    if end in str(line):
                        section_found = False
                    if section_found:
                        line = self._replace_keywords(line, obj,
                                                      data_size, data_offset)
                        inst_data += line
                    if begin in str(line):
                        exists_in_config = True
                        section_found = True

                    # will be last item processed but doesn't matter
                    type = obj['type']
            if not exists_in_config:
                resultOk = False
                resultMsg = f"'{ref_txt}' not found in config file"
            else:
                resultOk = True
                resultMsg = None

            # Return a dictionary with the result
            result = {
                'ref_txt': ref_txt,
                'type': type,
                'resultOk': resultOk,
                'badResultMsg': resultMsg
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
                for lineIndex, line in enumerate(config, start=1):
                    if end in str(line):
                        section_found = False
                    if section_found:
                        line = self._replace_keywords(line, obj,
                                                      data_size, data_offset)
                        inst_data += line
                    if begin in str(line):
                        exists_in_config = True
                        section_found = True

                    # will be last item processed but doesn't matter
                    type = obj['type']
            if not exists_in_config:
                resultOk = False
                resultMsg = f"'{ref_txt}' not found in config file"
            else:
                resultOk = True
                resultMsg = None

            # Return a dictionary with the result
            result = {
                'ref_txt': ref_txt,
                'type': type,
                'resultOk': resultOk,
                'badResultMsg': resultMsg
            }
        list_result.append(result)
        return inst_data

    @staticmethod
    def result(list_with_dicts, type='undefined'):
        """Check all result dicts and sum them, then print info to user"""
        rOkCnt = 0
        rBadCnt = 0
        print('\n')
        print(type)

        good_results = []  # Empty list
        bad_results = []  # Empty list

        for dict in list_with_dicts:
            if dict['resultOk']:
                good_results.append(dict['ref_txt'])
                rOkCnt += 1
            else:
                #  print(f"\t ERROR: {dict['badResultMsg']}")
                msg = f"\t ERROR: {dict['badResultMsg']}"
                bad_results.append(msg)
                rBadCnt += 1
        if rOkCnt > 0:
            print(f"\t Succesfully processed {rOkCnt} objects: {good_results}")

        if rBadCnt > 0:
            print("\n")
            print(f"\t {rBadCnt} resulted with error:")
            for r in bad_results:
                print('\t', r)

        if rOkCnt == 0 and rBadCnt == 0:
            print("\t Nothing processed")
