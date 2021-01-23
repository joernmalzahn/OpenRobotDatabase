# This file is part of the Open Robot Database by Jörn Malzahn available at https://github.com/joernmalzahn/OpenRobotDatabase. 
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
#
# The information in this file is provided "as is" without warranty of any kind. The maintainer of this file exercises reasonable efforts to 
# include accurate and up-to-date information; he, however, does not make any warranties or representations as to its accuracy or completeness. 
# Information in this file may periodically be added, changed, or updated without notice. 
# 
# If you make decisions based on the data provided in the Open Robot Database including any of its files, you do so at your own risk and it is strongly
# recommended to verify the information contained in this file through other channels.
#
# The information in this file is made available in the hope that it will be helpful to others. Contributions in the form of feedback, corrections, data, code, etc. is highly welcome and will 
# be credited. Please visit https://github.com/joernmalzahn/OpenRobotDatabase/blob/master/README.md on how to get in touch and provide feedback.

from ord_sql_interface import OrdSqlInterface
import yaml
import os
from functools import reduce
import matplotlib.pyplot as plt

import pandas as pd 


def dict_recursive_get(input_dict, address,default=None):
    """Recursive version of dict.get(key)
    Args:
        input_dict ([type]): [description]
        address ([type]): [description]

    Returns:
        [type]: [description]
    """
    result = reduce(lambda c,k: c.get(k,{}), address, input_dict)
    
    # Deal with empty fields
    if result == {}:
        result = None

    return result


class OrdCore:
    """
    Core class of the Open Cobot Database
    ... 

    Attributes
    ----------
    db_filename : str
        output DB file name
    ord_path : str
        path to open cobot library root
    output_type: {'row list', 'pandas'}
        determines the output type of the `get_data()`. The option 'row list' (default) corrsponds to 
        the standard output type used by `sqlite3.fetchall()`. The option 'pandas' converts this row 
        list into a pandas dataframe before returning the data.
    """
    _cobot_table_name = 'cobots'
    _manufacturer_table_name = 'manufacturers'

    def __init__(self,**kwargs):
        print("SQL Core Created!")
        self._db_filename = kwargs.get('db_filename', 'ord_database.db')
        self._overwrite_existing_db = kwargs.get('overwrite', True)
        self.output_type = kwargs.get('output_type', 'row list')
        
        # Path to Open Robot Database directory, make sure it ends with a separator
        self._db_file_path = kwargs.get('db_path', '.' + os.sep) 
        if self._db_file_path[-1] is not os.sep: 
            self._db_file_path += os.sep
        
        # Path to Open Robot Database directory, make sure it ends with a separator
        self.ord_path = kwargs.get('ord_path', os.path.dirname(__file__)) 
        if self.ord_path[-1] is not os.sep: 
            self.ord_path += os.sep

        # Load database configs
        print("The ord_core is located in {}.".format(self.ord_path))

        f = open(self.ord_path + "cobot_config.yaml",'r')
        yaml_content = yaml.load(f, Loader=yaml.FullLoader)
        self._cobot_fields = yaml_content["columns"]
        self._cobot_table_links = yaml_content["links"]
        f.close()

        f = open(self.ord_path + "manufacturer_config.yaml",'r')
        yaml_content = yaml.load(f, Loader=yaml.FullLoader)
        self._manufacturer_fields  = yaml_content["columns"]
        self._manufacturer_table_links = yaml_content["links"]
        f.close()

        # Derive additional paths
        self._manufacturer_path = self.ord_path + self._manufacturer_table_name + os.sep
        self._cobot_path = self.ord_path + self._cobot_table_name + os.sep
        
        self._sql_interface = OrdSqlInterface(self._db_file_path + self._db_filename)


        print('Manufacturer collection located in: %s' % self._manufacturer_path)
        print('Cobot collection located in %s' % self._cobot_path)



    def _create_tables(self):
        """
        Creates tables for cobots and manufacturers.
        """        
        # Manufacturer table
        self._sql_interface.create_table(self._manufacturer_table_name, self._manufacturer_fields, self._manufacturer_table_links)

        # Cobot table        
        self._sql_interface.create_table(self._cobot_table_name, self._cobot_fields, self._cobot_table_links)
        



    def _enter_cobot_data(self):

        allCobotYamls = os.listdir( self._cobot_path )

        key_list = list(self._cobot_fields.keys())
        value_list = list(self._cobot_fields.values())
        address_list = [value['address'] for value in value_list]

        for file in allCobotYamls:
            if file != "cobot_schema.yaml" and file != "cobot_template.yaml":
                with open( self._cobot_path + file) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)

                    # gather data
                    entry = list()

                    for key, address in zip(key_list, address_list) :
                        entry.append(dict_recursive_get(data, address + [key]) )

                    self._insert_cobot(tuple(entry))

    def _enter_manufacturer_data(self):

        allManufacturerYamls = os.listdir( self._manufacturer_path )
        
        key_list = list(self._manufacturer_fields.keys())
        value_list = list(self._manufacturer_fields.values())
        address_list = [value['address'] for value in value_list]

        for file in allManufacturerYamls:
            if file != "manufacturer_schema.yaml" and file != "manufacturer_template.yaml":
                with open( self._manufacturer_path + file) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)

                    # gather data
                    entry = list()

                    for key, address in zip(key_list, address_list) :
                        entry.append(dict_recursive_get(data, address + [key]) )


                    self._insert_manufacturer(tuple(entry))

    def get_manufacturer_id(self, manufacturer_name):

        return self._sql_interface.get_data(self._manufacturer_table_name,['id'], ['''name = \"''' + manufacturer_name + '''\"'''])[0][0]

    def _does_db_file_exist(self):
        return os.path.isfile(self._db_file_path + self._db_filename)


    def create_db(self):
        """
        Main routine to invoke the sqlite database file creation.
        """        

        # Check whether database file exists, if not, create one
        if self._does_db_file_exist():

            if not self._overwrite_existing_db:
                print('Database %s exists. Doing nothing.' % (self._db_file_path + self._db_filename))
                pass
            else:
                print('Database %s exists. Overwriting.' % (self._db_file_path + self._db_filename))
                os.remove(self._db_file_path + self._db_filename)

        print("Creating database tables.")
        self._create_tables()

        print("Inserting manufacturer data")
        self._enter_manufacturer_data()

        print("Inserting cobot data")
        self._enter_cobot_data()



    def get_all_cobots(self):
        """
        Query all rows in the cobots table
        :return: all cobot data
        """
        return self.get_data(self._cobot_table_name)

    def get_data(self, table, field_names = '*', where = None ):

        data = self._sql_interface.get_data(table, field_names, where)

        if self.output_type is 'pandas':

            if field_names is '*':
                columns = self.get_column_names(table)
            else:
                columns = field_names
            
            data = pd.DataFrame(data, columns = columns)

        return data


    def get_column_names(self, table):
        return self._sql_interface.get_column_names(table)

    def _insert_cobot(self, cobot):
        """
        Insert a new cobot into the cobots table
        :param cobot data:
        :return: cobot id
        """
        return self._sql_interface.insert_data_set(self._cobot_table_name, cobot, self._cobot_fields)

    def _insert_manufacturer(self, manufacturer):
        """
        Insert a new cobot into the cobots table
        :param cobot data:
        :return: cobot id
        """
        return self._sql_interface.insert_data_set(self._manufacturer_table_name, 
            manufacturer, 
            self._manufacturer_fields)

    


def main():
    
    # The name of our database will be:
    database = "ord_database.db"
    
    # Initialize the ORD core:
    core = OrdCore(db_filename=database)

    # Convert .yamls into a SQLite database
    core.create_db()        

    # Next we are going to plot the payload mass capacity for each robot 
    # versus the robot's maximum reach.

    # Extract and organize desired columns from the database
    data = core.get_data('cobots', ['payload mass', 'max reach'])
    payloads, reaches = zip(*data)
        
    # Plotting
    plt.plot(reaches, payloads,'o')
    ax = plt.gca()
    ax.set_xlim([0,1800])
    ax.set_ylim([0,26])
    ax.set_xlabel("Max. Reach [mm]")
    ax.set_ylabel("Payload Mass [kg]")
    plt.title("Number of Cobots: %d" % len(reaches))
    plt.show()

    data = core.get_data('manufacturers')
    print(data)

if __name__ == '__main__':
    main()


    
