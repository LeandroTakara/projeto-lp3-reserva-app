import mysql.connector

def open_connection(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def close_connection(connection):
    connection.close()

def insert_into(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract), table: str, *fields : str):
    cursor = connection.cursor()

    campos = '(' + fields[0]
    qtde_campos = len(fields)
    for i in range(1, qtde_campos):
        campo = fields[i]
        if(campo.__class__ == str):
            campos += f", '{fields[i]}'"
        else:
            campos += f", {fields[i]}"

    campos += ')'

    sql = f'INSERT INTO {table} VALUES {campos}'

    print(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()