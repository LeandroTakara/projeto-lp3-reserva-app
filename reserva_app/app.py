from flask import Flask, render_template, request
from save_load import save_csv, load_csv, get_room_id
from typing import Callable
from cadastrar_salas import cadastrar_uma_sala

def contains_register(registers: list[str], predicate: Callable[[], bool]) -> bool:
    for register in registers:
        if predicate(register):
            return True
    
    return False

LOCAL_DATABASE_USERS_PATH = 'csv-database/users.csv'
LOCAL_DATABASE_SALAS_RESERVADAS_PATH = "csv-database/salas_reservadas.csv"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_csv(LOCAL_DATABASE_USERS_PATH)

        correct_login = contains_register(users, lambda user: user[1] == email and user[2] == password)
        
        if correct_login:
            return render_template('reservas.html')

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

        user = [nome, email, password]

        save_csv(LOCAL_DATABASE_USERS_PATH, user)

        return render_template('login.html')

    raise Exception(f'Invalid {request.method} method in cadastro_page()')

@app.route('/reservas')
def reservas_page():
    return render_template('reservas.html')

@app.route('/reservar-sala', methods=['GET', 'POST'])
def reservar_sala_page():

    with open("./csv-database/rooms.csv", "r") as salinhas:

            lista_salas = []
            
            for salinha in salinhas:
            
                salinha_cheirosa = salinha.strip().split(",")
                lista_salas.append({"ID": salinha_cheirosa[0]})

    if request.method == 'GET':
        return render_template('reservar-sala.html', rooms_list = lista_salas)
    if request.method == 'POST':
        sala = request.form['sala']
        inicio = request.form['inicio']
        fim = request.form['fim']

        sala_cadastrada = [sala,inicio,fim]
        save_csv(LOCAL_DATABASE_SALAS_RESERVADAS_PATH, sala_cadastrada)

        sala_cadastrada[1] = sala_cadastrada[1].replace("T", " - ")
        sala_cadastrada[2] = sala_cadastrada[2].replace("T", " - ")

        sala_cadastrada = [{
            "sala" : sala_cadastrada[0],
            "inicio" : sala_cadastrada[1],
            "fim" : sala_cadastrada[2]
        }]

        return render_template('reserva/detalhe-reserva.html', reserve_details = sala_cadastrada)

@app.route('/listar-salas')
def listar_salas_page():

    lista_salas = []

    with open("./csv-database/rooms.csv", "r") as salinhas:
        for salinha in salinhas:
        
            salinha_cheirosa = salinha.strip().split(",")
            lista_salas.append({"ID": salinha_cheirosa[0],"tipo": salinha_cheirosa[1], "capacidade": salinha_cheirosa[2], "descricao": salinha_cheirosa[3], "ativa":salinha_cheirosa[4]})

    return render_template('listar-salas.html', rooms_list = lista_salas)

@app.route('/cadastrar-sala', methods= ['GET','POST'])
def cadastrar_sala_page():

    if request.method == 'GET':
        return render_template('cadastrar-sala.html')
    
    if request.method == 'POST':
    
        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]
        ide = get_room_id()
        
        sala_cadastrada = {"ID": ide, "tipo":tipo, "capacidade":capacidade, "descricao":descricao, "ativa": "Sim"}
        cadastrar_uma_sala(sala_cadastrada)

        return render_template('cadastrar-sala.html')

@app.route('/reserva/detalhe-reserva')
def reserva_detalhe_reserva_page():
    return render_template('reserva/detalhe-reserva.html')

if __name__ == '__main__':
    app.run(debug=True)