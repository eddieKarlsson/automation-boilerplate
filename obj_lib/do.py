    def td_gen_do(self):
        """Create and concetenate all text lines to different files"""
        # setup variables
        config_file = os.path.join(s.CONFIG_PATH, 'Config_DO.txt')
        sheet = 'DO'

        # Check what output path to use, if 'None' create in current directory, otherwise as specified
        if self.output_path is None:
            file_path = 'Generated DO'
        elif self.output_path == OUTPUT_PATH_START_VALUE:
            file_path = 'Generated DO'
        else:
            file_path = os.path.join(self.output_path, 'Generated DO')
        # Create sub-directory if it doesn't exist
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # PLC function, concatenate data
        header_data = self.td_single(config_file, 'header')
        var_data = self.td_multiple(config_file, 'var', sheet)
        func_header_data = self.td_single(config_file, 'funcHeader')
        codebody_data = self.td_multiple(config_file, 'codebody', sheet)
        footer_data = self.td_single(config_file, 'footer')

        # Create file and put it inside path created above
        filename = 'PLC_' + sheet + '.awl'
        file_and_path = os.path.join(file_path, filename)
        with open(file_and_path, 'w', encoding='cp1252') as functionFile:
            data = header_data
            data += var_data
            data += func_header_data
            data += codebody_data
            data += footer_data
            functionFile.write(data)
            print(filename, 'created')
            logging.info(filename + ' created')

        # PLC Datablock, if all elements exists concatenate data and create file
        db_header_data = self.td_single(config_file, 'db_header')
        db_var_data = self.td_multiple(config_file, 'db_var', sheet)
        db_footer_data = self.td_single(config_file, 'db_footer')
        if db_header_data != '' and db_var_data != '' and db_footer_data != '':
            filename = 'PLC_' + sheet + '_DB.db'
            file_and_path = os.path.join(file_path, filename)
            with open(file_and_path, 'w', encoding='cp1252') as dbFile:
                data = db_header_data
                data += db_var_data
                data += db_footer_data
                dbFile.write(data)
                print(filename, 'created')
                logging.info(filename + ' created')

        # PLC symbol table
        symbol_data = self.td_multiple(config_file, 'symbol', sheet)
        if symbol_data != '':
            filename = 'PLC_' + sheet + '_Symbol.sdf'
            file_and_path = os.path.join(file_path, filename)
            with open(file_and_path, 'w', encoding='cp1252') as symbolFile:
                symbolFile.write(symbol_data)
                print(filename, 'created')
                logging.info(filename + ' created')

        # Intouch
        it_data = self.td_multiple(config_file, 'Intouch', sheet, start_index=s.DO_START_INDEX)
        if it_data != '':
            filename = 'IT_' + sheet + '.csv'
            file_and_path = os.path.join(file_path, filename)
            with open(file_and_path, 'w', encoding='cp1252') as itFile:
                itFile.write(it_data)
                print(filename, 'created')
                logging.info(filename + ' created')
        print('Generated files put in...', file_path)
        logging.info('Generated DO files put in ' + file_path)
