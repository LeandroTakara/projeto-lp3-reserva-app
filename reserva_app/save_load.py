from csv import writer, reader

def save_csv(file: str, data: list[str]) -> None:
    '''
        Salva os dados em um arquivo csv

        :param file: nome do arquivo
        :param data: lista de string para salvar
    '''
    
    with open(file, 'a', encoding='utf-8') as f:
        csv_writer = writer(f, lineterminator='\n')

        csv_writer.writerow(data)

def load_csv(file: str) -> list[str]:
    '''
        Carrega os dados de um arquivo csv

        :param file: nome do arquivo
        :returns: registros do arquivo csv
    '''

    rows = []

    with open(file, 'r', encoding='utf-8') as f:
        csv_reader = reader(f)

        for row in csv_reader:
            rows.append(row)

    return rows

