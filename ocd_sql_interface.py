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
            print(sqlite3.version)
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

    def create_table(self, create_table_sql):
        """ Create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        self._create_connection()
        try:
            c = self._conn.cursor()
            c.execute(create_table_sql)

        except Error as e:
            print(e)

    def insert_data_set(self, table, dataset):
        """
        Insert a new cobot into the cobots table
        :param conn:
        :param cobot:
        :return: cobot id
        """
        sql_string = ''' INSERT INTO '''+ table + '''(
                    name,
                    manufacturer,
                    payload_mass,
                    max_reach,
                    robot_mass,
                    videos,
                    website)
                VALUES(?,?,?,?,?,?,?) '''

        self._create_connection()

        cur = self._conn.cursor()
        cur.execute(sql_string, dataset)
        self._conn.commit()

        self._close_connection()

        return cur.lastrowid  

    def retrieve_data(self, sql_string):

        self._create_connection()

        cur = self._conn.cursor()
        cur.execute(sql_string)

        rows = cur.fetchall()

        for row in rows:
            print(row)

        self._close_connection()

        return rows

