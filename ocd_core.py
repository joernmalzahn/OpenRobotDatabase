from ocd_sql_interface import OcdSqlInterface
import yaml
import os
from functools import reduce
import matplotlib.pyplot as plt


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
            'address': [], 
            'attribute': 'text NOT NULL'
            },
        'manufacturer' : {
            'address': [], 
            'attribute': 'text NOT NULL'
            },
        'payload mass' : {
            'address': ['mechanical properties'],
            'attribute': 'integer NOT NULL'
            },
        'max reach' : {
            'address': ['mechanical properties'],
            'attribute': 'integer NOT NULL'
            },
        'robot mass' : {
            'address': ['mechanical properties'],
            'attribute':  'integer'
            },
        'videos' : {
            'address': [],
            'attribute': 'text'
            },
        'website' : {
            'address': [], 
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
        self._sql_interface.create_table(self._cobot_table_name, self._cobot_fields)
        
        # Manufacturer table - to be implemented

    def _enter_cobot_data(self):

        allCobotYamls = os.listdir( self._cobot_dir )
        print(allCobotYamls)
        
        key_list = list(self._cobot_fields.keys())
        value_list = list(self._cobot_fields.values())
        address_list = [value['address'] for value in value_list]

        for file in allCobotYamls:
            if file != "cobot_schema.yaml" and file != "cobot_template.yaml":
                with open( self._cobot_dir + file) as f:
                    print(file)
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    print(data)

                    # gather data
                    cobot_entry = list()

                    for key, address in zip(key_list, address_list) :
                        cobot_entry.append(dict_recursive_get(data, address + [key]) )


                    self._insert_cobot(tuple(cobot_entry))


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

        return self._sql_interface.get_data(table, field_names)


    def _insert_cobot(self, cobot):
        """
        Insert a new cobot into the cobots table
        :param cobot data:
        :return: cobot id
        """
        return self._sql_interface.insert_data_set(self._cobot_table_name, cobot, self._cobot_fields)

    def _insert_manufacturer(self, manufacturer):
        """
        Insert a new manufacturer into the manufacturer table
        :param manufacturer data:
        :return: manufacturer id
        """
        return self._sql_interface.insert_data_set(self._manufacturer_table_name, manufacturer)


def main():
    
    # The name of our database will be:
    database = "ocd_database.db"
    
    # Initialize the OCD core:
    core = OcdCore(database)

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


if __name__ == '__main__':
    main()


    
