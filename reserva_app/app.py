from flask import Flask, render_template, redirect, request
from typing import Callable
from .save_load import save_csv, load_csv
from .connection import open_connection, close_connection, insert_into

def get_room_id():
    with open(NEXT_ID_PATH, 'r') as room_id:
        ide = int(room_id.read())
        
    with open(NEXT_ID_PATH, 'w') as room_id:
        room_id.write(f"{ide+1}")

    return ide

def get_reserve_id():
    with open(NEXT_RESERVE_ID_PATH, 'r') as reserve_id:
        ide = int(reserve_id.read())
        
    with open(NEXT_RESERVE_ID_PATH, 'w') as reserve_id:
        reserve_id.write(f"{ide+1}")

    return ide

def contains_register(registers: list[str], predicate: Callable[[], bool]) -> bool:
    for register in registers:
        if predicate(register):
            return [True, register[0]]
    
    return [False]

NEXT_ID_PATH = './csv-database/room_id.csv'
NEXT_RESERVE_ID_PATH = './csv-database/reserve_id.csv'

LOCAL_DATABASE_USERS_PATH = 'csv-database/users.csv'
LOCAL_DATABASE_RESERVED_ROOMS_PATH = 'csv-database/salas_reservadas.csv'
LOCAL_DATABASE_ROOMS_PATH = 'csv-database/rooms.csv'

user_logged_name = "MANDIOCA"

HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'ReservaApp'

con = open_connection(HOST, USER, PASSWORD, DATABASE)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    global user_logged_name
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_csv(LOCAL_DATABASE_USERS_PATH)

        return_of_register = contains_register(users, lambda user: user[1] == email and user[2] == password)

        correct_login = return_of_register[0]
        
        if correct_login:
            user_logged_name = return_of_register[1]
            return redirect('reservas')

        return render_template('login.html')

    raise Exception(f'Invalid {request.method} method in login_page()')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'GET':
        return render_template('cadastro.html')

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']

        users = load_csv(LOCAL_DATABASE_USERS_PATH)

        if contains_register(users, lambda user: user[1] == email)[0]:
            return render_template('cadastro.html')

        user = [nome, email, password]

        save_csv(LOCAL_DATABASE_USERS_PATH, user)

        return render_template('login.html')
    
    raise Exception(f'Invalid {request.method} method in cadastro_page()')

@app.route('/reservas')
def reservas_page():
    return render_template('reservas.html')

@app.route('/reservar-sala', methods=['GET', 'POST'])
def reservar_sala_page():
    global user_logged_name

    if request.method == 'GET':
        lista_salas = []

        for room in load_csv(LOCAL_DATABASE_ROOMS_PATH):
            lista_salas.append({ 'ID': room[0] })

        return render_template('reservar-sala.html', rooms_list = lista_salas)

    if request.method == 'POST':
        sala = request.form['sala']
        inicio = request.form['inicio']
        fim = request.form['fim']
        idezim = str(get_reserve_id())

        sala_cadastrada = [idezim,sala,inicio,fim]
        save_csv(LOCAL_DATABASE_RESERVED_ROOMS_PATH, sala_cadastrada)

        sala_cadastrada[2] = sala_cadastrada[2].replace('T', ' - ')
        sala_cadastrada[3] = sala_cadastrada[3].replace('T', ' - ')

        sala_cadastrada = {
            'ID' : sala_cadastrada[0].zfill(3),
            'sala' : sala_cadastrada[1],
            'inicio' : sala_cadastrada[2],
            'fim' : sala_cadastrada[3]
        }

        return render_template('reserva/detalhe-reserva.html', reserve_details = sala_cadastrada, nome_usuario = user_logged_name)

@app.route('/listar-salas')
def listar_salas_page():
    lista_salas = []

    for room in load_csv(LOCAL_DATABASE_ROOMS_PATH):
        lista_salas.append({ 'ID': room[0], 'tipo': room[1], 'capacidade': room[2], 'descricao': room[3], 'ativa':room[4] })

    return render_template('listar-salas.html', rooms_list = lista_salas)

@app.route('/cadastrar-sala', methods= ['GET','POST'])
def cadastrar_sala_page():
    if request.method == 'GET':
        return render_template('cadastrar-sala.html')
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        capacidade = request.form['capacidade']
        descricao = request.form['descricao']

        if not tipo or not capacidade or not descricao:
            return render_template('cadastrar-sala.html')

        ide = get_room_id()

        room = [str(ide), tipo, capacidade, descricao, 'Sim']

        save_csv(LOCAL_DATABASE_ROOMS_PATH, room)

        insert_into(con, 'rooms', tipo, capacidade, True)

        return render_template('cadastrar-sala.html')

@app.route('/reserva/detalhe-reserva')
def reserva_detalhe_reserva_page():
    return render_template('reserva/detalhe-reserva.html')

if __name__ == '__main__':
    app.run(debug=True)
