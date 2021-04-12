import sqlite3

def fetch_data(cursor, data):
    cursor.execute("SELECT * FROM executions WHERE execution_id=?", (data,))
    return cursor.fetchall()

def db_lookup(cursor):
    cursor.execute("SELECT * FROM executions")
    return cursor.fetchall()

def insert_data(connection, cursor, data):
    sql ="INSERT INTO executions(execution_id, time) VALUES(?,?)"
    cursor.execute(sql, (data))
    connection.commit()

def delete_data(connection, cursor, data):
    sql = 'DELETE FROM executions WHERE execution_id=?'
    cursor.execute(sql, (data,))
    connection.commit()
    
def update_data(connection, cursor, data):
    sql = "UPDATE executions SET time=? WHERE execution_id=?"
    cursor.execute(sql, (data))
    connection.commit()

def initialize_database():
    connection = sqlite3.connect('reach_engine:cachedb?mode=memory&cache=shared')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS executions")
    cursor.execute("CREATE TABLE executions(execution_id TEXT PRIMARY KEY, time REAL)")
    cursor.execute("INSERT INTO executions(execution_id, time) VALUES(?,?)", ("timeout", 90,))
    connection.commit()
    return connection, cursor