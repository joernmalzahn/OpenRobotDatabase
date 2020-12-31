import sqlite3
from sqlite3 import Error

class OcdSqlInterface:
    """ Classe handling all the db file interactions """

    def __init__(self, db_filename='ocd_database.db'):
        self._conn = None
        self._db_file_name = db_filename

    def _create_connection(self):
        """ Create a database connection to the SQLite database
            specified by the db_file_name property
        """
        try:
            self._conn = sqlite3.connect(self._db_file_name)
        except Error as e:
            print("Error")
            print(e)

    def _close_connection(self):
        """ Close a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        if self._conn:
            self._conn.close()
            self._conn = []
    

    def create_table(self, table_name, fields, links):
        """ Create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        create_table_sql = self._get_sql_create_table_string(table_name, fields, links)

        self._create_connection()
        try:
            c = self._conn.cursor()
            c.execute(create_table_sql)

        except Error as e:
            print(e)

        self._conn.commit()
        self._close_connection()

    def make_data_compatible(self, dataset):

        # SQLite3 does not support array type entries. So convert any array in the data to a string representing the array.
        # This will be a comma separated list that can be parsed later on if necessary.
        compatible_dataset = [ str(element) if isinstance(element, list) else element for element in dataset ]       
        return compatible_dataset

    def _get_sql_create_table_string(self, table_name, fields, links = {}):
        
        sql_create_table = "CREATE TABLE " + table_name + """ (\n\tid integer PRIMARY KEY,\n\t"""
        sql_create_table += ',\n\t'.join(
            '\"' + key + '\" ' + fields[key]['attribute'] 
             if ' ' in key else 
             key + ' ' + fields[key]['attribute'] 
             for key in fields
            )

        # Add links to other tables    
        if bool(links): # if links is not empty
            for table_name in links:
                local_column_name = links[table_name]['local_column'];
                remote_column_name = links[table_name]['remote_column'];
                sql_create_table += ",\n"
                sql_create_table +=  "FOREIGN KEY (" + local_column_name + ") REFERENCES " + table_name + " ( " + remote_column_name + " )" 
        
        sql_create_table += "\n);"        

        return sql_create_table

    def _get_sql_select_string(self, table, field_names, where = None):

        sql_string = "SELECT "
        sql_string += ', '.join('\"' + field + '\"' if ' ' in field else field for field in field_names)
        sql_string += " FROM " + table 

        if where is not None:

            sql_string += " WHERE "
            sql_string += ', '.join( where_field for where_field in where)
        
        return sql_string

    def _get_sql_insert_string(self, table_name, fields):
                
        sql_string = "INSERT INTO " + table_name + " (\n\t"
        sql_string +=  ',\n\t'.join('\"' + key + '\"' if ' ' in key else key for key in fields) 
        sql_string += '\n)VALUES({})'.format(','.join('?' * len(fields)))
        
        return sql_string

    def insert_data_set(self, table, dataset, fields):
        """
        Insert a new cobot into the cobots table
        :param conn:
        :param cobot:
        :return: cobot id
        """
        sql_string = self._get_sql_insert_string(table,fields)
        compatible_dataset = self.make_data_compatible(dataset)

        self._create_connection()

        cur = self._conn.cursor()
        cur.execute(sql_string, compatible_dataset)
        self._conn.commit()

        self._close_connection()

        return cur.lastrowid  

    def get_data(self,  table, field_names, where = None):

        sql_string = self._get_sql_select_string(table, field_names, where)
        self._create_connection()

        cur = self._conn.cursor()
        cur.execute(sql_string)

        rows = cur.fetchall()

        self._close_connection()

        return rows

    def get_column_names(self, table):

        self._create_connection()
        cursor = self._conn.execute('select * from ' + table)
        
        names = [description[0] for description in cursor.description]

        return names
