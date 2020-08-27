from ocd_sql_interface import OcdSqlInterface
import yaml
import os
from functools import reduce


def dict_recursive_get(input_dict, address):
    """Recursive version of dict.get(key)
    Args:
        input_dict ([type]): [description]
        address ([type]): [description]

    Returns:
        [type]: [description]
    """
    return reduce(lambda c,k: c.get(k,{}), address, input_dict)


def fields_2_keys(input_dict):
    """Splits a field definition table into lists of keys, field addesses and attributes.
    
    Args:
        input_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    key_list = list(input_dict.keys())
    value_list = list(input_dict.values())
    attribute_list = [value['attribute'] for value in value_list]
    address_list = [value['address'] for value in value_list]

    return key_list, address_list, attribute_list


class OcdCore:
    """
    Core class of the Open Cobot Database
    ... 

    Attributes
    ----------
    db_filename : str
        output DB file name
    ocd_path : str
        path to open cobot library root
    """
    _cobot_table_name = 'cobots'
    _manufacturer_table_name = 'manufacturers'
    _cobot_dir = _cobot_table_name  + os.sep
    _manufacturer_dir = _manufacturer_table_name  + os.sep
    
    _cobot_fields = {
        'name' : {
            'address': [''], 
            'attribute': 'text NOT NULL'
            },
        'manufacturer' : {
            'address': [''], 
            'attribute': 'text NOT NULL'
            },
        'payload_mass' : {
            'address': ['mechanical properties'],
            'attribute': 'integer NOT NULL'
            },
        'max_reach' : {
            'address': ['mechanical properties'],
            'attribute': 'integer NOT NULL'
            },
        'robot_mass' : {
            'address': ['mechanical properties'],
            'attribute':  'integer'
            },
        'videos' : {
            'address': [''],
            'attribute': 'text'
            },
        'website' : {
            'address': [''], 
            'attribute': 'text NOT NULL'}
    }

    def __init__(self,db_filename='ocd_database.db'):
        print("SQL Core Created!")
        self._db_filename = db_filename
        self.ocd_path = '.' + os.sep
        self._manufacturer_path = self.ocd_path + self._manufacturer_dir
        self._cobot_path = self.ocd_path + self._cobot_dir
        self._sql_interface = OcdSqlInterface(db_filename)

        if not os.path.isfile(db_filename):
            print('Database %s not found. Creating new file' % db_filename)
            self.create_db()
            

        print('Manufacturer collection located in: %s' % self._manufacturer_path)
        print('Cobot collection located in %s' % self._cobot_path)

    def _create_tables(self):
        """
        Creates tables for cobots and manufacturers.
        """        
        # Cobot table        
        sql_create_cobot_table = "CREATE TABLE IF NOT EXISTS " + self._cobot_table_name + """ (\n\tid integer PRIMARY KEY"""
        for tmp in self._cobot_fields:
            sql_create_cobot_table += ',\n\t' + tmp + ' ' + self._cobot_fields[tmp]['attribute']
        sql_create_cobot_table += "\n);"

        self._sql_interface.create_table(sql_create_cobot_table)
        
        # Manufacturer table - to be implemented

    def _enter_cobot_data(self):

        allCobotYamls = os.listdir( self._cobot_dir )
        print(allCobotYamls)
        
        for file in allCobotYamls:
            if file != "cobot_schema.yaml" and file != "cobot_template.yaml":
                with open( self._cobot_dir + file) as f:
                    print(file)
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    print(data)

                    # gather data, this is the part that will need care to ensure data consistency... more work needed here...
                    cobot_entry = (
                        data['name'],
                        data['manufacturer'],
                        data['mechanical properties']['payload mass'],
                        data['mechanical properties']['max reach'],
                        data.get('mechanical properties').get('robot masss', None),
                        data['videos'][0],
                        data['website'][0]
                        )


#                    cobot_entry_alternative = 

                    
                    self._insert_cobot(cobot_entry)


    def create_db(self):
        """
        Main routine to invoke the sqlite database file creation.
        """        
        #print("Creating database connection.")
        #self._sql_interface._create_connection(self._db_filename)

        print("Creating database tables.")
        self._create_tables()

        print("Inserting cobot data")
        self._enter_cobot_data()


    def get_all_cobots(self):
        """
        Query all rows in the cobots table
        :return: all cobot data
        """
        return self.get_data(self._cobot_table_name)

    def get_data(self, table, field_names = '*' ):
        sql_string = 'SELECT '
        if len(field_names) > 1:
            for tmp in field_names[0:-1]:
                sql_string += tmp + ', '       
        
        sql_string += field_names[-1] + " FROM " + table

        return self._sql_interface.retrieve_data(sql_string)


    def _insert_cobot(self, cobot):
        """
        Insert a new cobot into the cobots table
        :param cobot data:
        :return: cobot id
        """
        return self._sql_interface.insert_data_set(self._cobot_table_name, cobot)

    def _insert_manufacturer(self, manufacturer):
        """
        Insert a new manufacturer into the manufacturer table
        :param manufacturer data:
        :return: manufacturer id
        """
        return self._sql_interface.insert_data_set(self._manufacturer_table_name, manufacturer)


def main():
    database = "test.db"
    
    core = OcdCore()
    core.create_db()        


if __name__ == '__main__':
    main()


    
