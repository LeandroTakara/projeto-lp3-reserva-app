import csv

def cadastrar_uma_sala(sala):
    with open("./csv-database/rooms.csv", "a") as arquivo_salas:
        arquivo_salas.write(f"{sala['tipo']},{sala['capacidade']},{sala['descricao']}\n")