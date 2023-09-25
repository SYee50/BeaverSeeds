import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv


# Set the variables for db connection with .env variables
load_dotenv(find_dotenv())
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    '''
    connects to a MySQL database using the db variables declared in this module,
    or the provided host, user, passwd, and db variables, and returns a MySQLdb 
    connection object.
    '''
    db_connection = MySQLdb.connect(host,user,passwd,db)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object
    query: an SQL query string
    query_params: an optional tuple, containing the parameters to send with the query

    returns: a Cursor Object
    '''

    # Handle Errors, no connection, or no query passed in
    if db_connection is None:
        print("No connection to the database. Try calling connect_to_database().")
        return None
    if query is None or len(query.strip()) == 0:
        print("query is empty. You must pass in an SQL query.")
        return None
    
    print("Executing %s with %s" % (query, query_params))

    # Create a cursor, execute and commit the query
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit()
    return cursor

    