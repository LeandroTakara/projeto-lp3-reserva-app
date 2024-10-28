from flask import Flask, render_template, redirect, request
from typing import Callable
from .connection import open_connection, insert_into, select_user_ID, select_last_ID, select_rooms, select_rooms_ID, select_users

def contains_register(registers: list[str], predicate: Callable[[], bool]) -> bool:
    for register in registers:
        if predicate(register):
            return [True, register[0]]
    return [False]

user_logged_name = "MANDIOCA"

HOST = 'localhost'
USER = 'root'
PASSWORD = 'bito132'
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

        users = select_users(con)

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

        users = select_users(con)

        if contains_register(users, lambda user: user[1] == email)[0]:
            return render_template('cadastro.html')

        insert_into(con, 'usuarios', 'DEFAULT', nome, email, password)

        return render_template('login.html')
    
    raise Exception(f'Invalid {request.method} method in cadastro_page()')

@app.route('/reservas')
def reservas_page():
    return render_template('reservas.html')

@app.route('/reservar-sala', methods=['GET', 'POST'])
def reservar_sala_page():
    global user_logged_name

    if request.method == 'GET':
        return render_template('reservar-sala.html', rooms_list = select_rooms_ID(con))

    if request.method == 'POST':
        sala = request.form['sala']
        inicio = request.form['inicio']
        fim = request.form['fim']
        idezim = select_last_ID(con) + 1

        sala_cadastrada = [idezim,sala,inicio,fim]

        sala_cadastrada[2] = sala_cadastrada[2].replace('T', ' - ')
        sala_cadastrada[3] = sala_cadastrada[3].replace('T', ' - ')

        sala_cadastrada = {
            'ID' : str(sala_cadastrada[0]).zfill(3),
            'sala' : sala_cadastrada[1],
            'inicio' : sala_cadastrada[2],
            'fim' : sala_cadastrada[3]
        }
        
        sala = int(sala)
        id_usuario_atual = select_user_ID(con, user_logged_name)

        insert_into(con, 'reservas', 'DEFAULT', inicio, fim, id_usuario_atual, sala)

        return render_template('reserva/detalhe-reserva.html', reserve_details = sala_cadastrada, nome_usuario = user_logged_name)

@app.route('/listar-salas')
def listar_salas_page():
    return render_template('listar-salas.html', rooms_list = select_rooms(con))

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

        insert_into(con, 'rooms', 'DEFAULT', tipo, descricao, capacidade, True)

        return render_template('cadastrar-sala.html')

@app.route('/reserva/detalhe-reserva')
def reserva_detalhe_reserva_page():
    return render_template('reserva/detalhe-reserva.html')

if __name__ == '__main__':
    app.run(debug=True)