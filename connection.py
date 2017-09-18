import sqlite3

db_file = "db/currencies.db"

def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def select_all_currencies():
    """
    Query all rows in the currencies table
    :param conn: the Connection object
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    return rows
