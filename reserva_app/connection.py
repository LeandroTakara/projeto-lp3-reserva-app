import mysql.connector

def open_connection(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def close_connection(connection):
    connection.close()

def insert_into(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract), table: str, room_type: str, capacity: int, active: bool):
    cursor = connection.cursor()
    sql = f'INSERT INTO {table} VALUES (DEFAULT, %s, %s, %s)'
    cursor.execute(sql, (room_type, capacity, active))
    connection.commit()
    cursor.close()
