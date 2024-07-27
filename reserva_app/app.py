from flask import Flask, render_template, request
from save_load import save_csv, load_csv
from typing import Callable

def contains_register(registers: list[str], predicate: Callable[[], bool]) -> bool:
    for register in registers:
        if predicate(register):
            return True
    
    return False

LOCAL_DATABASE_USERS_PATH = 'csv-database/users.csv'
LOCAL_DATABASE_SALAS_RESERVADAS_PATH = "csv-database\salas_reservadas.csv"

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
    if request.method == 'GET':
        return render_template('reservar-sala.html')
    if request.method == 'POST':
        sala = request.form['sala']
        inicio = request.form['inicio']
        fim = request.form['fim']

        sala_cadastrada = [sala,inicio,fim]
        save_csv(LOCAL_DATABASE_SALAS_RESERVADAS_PATH, sala_cadastrada)
        return render_template('reserva/detalhe-reserva.html')

@app.route('/listar-salas')
def listar_salas_page():
    return render_template('listar-salas.html')

@app.route('/cadastrar-sala')
def cadastrar_sala_page():
    return render_template('cadastrar-sala.html')

@app.route('/reserva/detalhe-reserva')
def reserva_detalhe_reserva_page():
    return render_template('reserva/detalhe-reserva.html')

if __name__ == '__main__':
    app.run(debug=True)
