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
    
def select_user_ID(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract), name : str):
    cursor = connection.cursor(dictionary=True)

    sql = f"SELECT * FROM usuarios WHERE nome = '{name}'"

    print(F"MACACO {sql}")
    cursor.execute(sql)
    r = None
    for result in cursor:
        r = result['ID']
    cursor.close()

    return r

def select_last_ID(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract)):
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT MAX(ID) FROM reservas"

    cursor.execute(sql)
    
    for result in cursor:
        r = result['MAX(ID)']
    cursor.close()

    if(r is None):
        r = 0

    return r

def select_rooms(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract)):
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT * FROM rooms"
    resposta = []

    cursor.execute(sql)
    for result in cursor:
        resposta.append({ 'ID': result['ID'], 'tipo': result['tipo_sala'], 'capacidade': result['capacidade'], 'descricao': result['descricao'], 'ativa': result['ativo']})
    cursor.close()

    return resposta

def select_rooms_ID(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract)):
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT ID FROM rooms"
    resposta = []

    cursor.execute(sql)
    for result in cursor:
        resposta.append({'ID': result['ID']})
    cursor.close()

    return resposta

def select_users(connection: (mysql.connector.pooling.PooledMySQLConnection | mysql.connector.connection.MySQLConnectionAbstract)):
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios"
    resposta = []

    cursor.execute(sql)
    for result in cursor:
        resposta.append([result['nome'], result['email'], result['senha']])
    cursor.close()

    return resposta