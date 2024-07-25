from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_page_by_post():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')

@app.route('/reservas')
def reservas_page():
    return render_template('reservas.html')

@app.route('/reservas', methods=['POST'])
def reservas_page_by_post():
    email = request.form['email']
    password = request.form['password']

    return render_template('reservas.html')

@app.route('/reservar-sala')
def reservar_sala_page():
    return render_template('reservar-sala.html')

@app.route('/listar-salas')
def listar_salas_page():
    return render_template('listar-salas.html')

@app.route('/cadastrar-sala')
def cadastrar_sala_page():
    return render_template('cadastrar-sala.html')

@app.route('/reserva/detalhe-reserva')
def reserva_detalhe_reserva_page():
    return render_template('reserva/detalhe-reserva.html')
