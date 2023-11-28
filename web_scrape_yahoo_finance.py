# Web scraper para resgatar dados referente ao valor da ação ação de empresas por meio do 'Yahoo! Finance' através de
# sua página 'https://finance.yahoo.com/'. Neste mesmo arquivo é feito a chamada ao web scraper de market cap e os dados
# são armazenados em um arquivo .txt em forma de lista

import datetime as dt
import pandas as pd
import ast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from web_scrape_marketcap import check_marketcap
import os


# Para acessar a query desejada é necessário adaptar a data para o formato utilizado pela plataforma em sua URI
def check_params_data(date):
    # O formato utilizado pelo yahoo finance é uma medida de segundos da data desejada, iniciando a contagem a partir
    # de 1º de janeiro de 1970
    data_zero = dt.datetime(1970, 1, 1)
    date = date.split('-')
    date = [int(_) for _ in date]

    date = dt.datetime(date[0], date[1], date[2])

    range_sete_dias = (7 * 86400)

    data_3_meses = date + relativedelta(months=3)

    # Foi realizada a consulta do valor da ação 3 meses após o contrato, mas esse dado acabou não sendo utilizado
    # posteriormente
    query_p1 = (date - data_zero).total_seconds() - range_sete_dias
    query_p2 = (data_3_meses - data_zero).total_seconds()

    return [int(query_p1), int(query_p2)]


# Resgatando as tags das empresas presentes no arquivo .txt por meio de uma leitura literal do arquivo como uma lista
with open("empresas_confirmadas_tags.txt", "r") as f2:
    txt_names = [ast.literal_eval(line) for line in f2.read().splitlines()]

# Configurações do Selenium
options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options)


# Pasta onde os dados filtrados estão armazenados
data_directory = "Dados-filtrados"

for file in os.listdir(data_directory):
    file_path = os.path.join(data_directory, file)

    file1 = pd.read_csv(filepath_or_buffer=file_path, low_memory=False, on_bad_lines='warn')

    names = file1['recipient_name_raw'].apply(str)



    # O counter é utilizado apenas como indicador de quantos contratos foram consultados caso haja uma falha
    counter = 0


    for j in range(len(txt_names)):
        # txt_names é uma lista de listas no seguinte formato:
        # [['nome da empresa', 'símbolo da empresa no mercado de ações], ...]
        NAME = txt_names[j][0]
        tag = txt_names[j][1]

        # Facilitar a identificação de onde parou em caso de falha
        print(f"{NAME} - {tag} - {j}")

        # Arquivo que será criado para cada empresa e nomeado utilizando o seu símbolo no mercado de ações
        f3 = open(f"Dados-Web-Scraping/{tag}.txt", "a")

        # Máscara que será aplicada para consultar todos contratos que possuem o nome (que é uma parte reduzida do nome
        # completo da empresa e está armazenado em 'NAME') da empresa que foi armazenado no arquivo .txt
        mask = names.apply(lambda x: NAME in x)

        filtered_rows = file1[mask]

        # Retirando dados do valor do contrato e da data em seu formato originalmente armazenado
        a = list(filtered_rows['total_dollars_obligated'])
        b = list(filtered_rows['action_date'])

        c = []

        # Armazenando a data e o valor em uma lista nomeada 'c'
        for i in range(len(a)):
            counter += 1
            c.append([b[i], a[i]])

        # Ordenando a lista pela data do contrato
        c.sort(key=lambda x: x[0])

        # Para cada contrato existente dentro desta lista
        for i in range(len(c)):

            contract_date = str(c[i][0])

            # Usando a função para resgatar as datas formatadas
            params = check_params_data(contract_date)

            uri = (f'https://finance.yahoo.com/quote/{tag}/history?period1={params[0]}&period2={params[1]}&interval=1d&'
                   f'filter=history&frequency=1d&includeAdjustedClose=true')


            driver.get(uri)

            table = driver.find_elements(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr')

            # Caso não haja dados referentes a empresa ou a data especificada
            if len(table) < 1:
                pass

            else:
                # Os condicionais são para garantir que o dado resgatado seja o esperado, e se não for ele retira da
                # proxima linha
                row1 = table[-1].find_elements(By.TAG_NAME, 'td')
                if len(row1) < 7:
                    row1 = table[-2].find_elements(By.TAG_NAME, 'td')

                row2 = table[-15].find_elements(By.TAG_NAME, 'td')
                if len(row2) < 7:
                    row2 = table[-16].find_elements(By.TAG_NAME, 'td')

                row3 = table[0].find_elements(By.TAG_NAME, 'td')
                if len(row3) < 7:
                    row3 = table[1].find_elements(By.TAG_NAME, 'td')

                # Resgatando dados de market cap a partir do web scraper de market cap
                marketcap = check_marketcap(tag, contract_date)

                # Da esquerda para a direita, os dados sendo gravados são:
                # [Data de emissão do contrato, valor do contrato, valor da ação 7 dias antes do contrato ser emitido,
                # valor da ação 7 dias depois, valor da ação 3 meses depois e valor do market cap da empresa]
                f3.write(f"{[contract_date, c[i][1], row1[2].text, row2[2].text, row3[2].text, marketcap]}\n")

        f3.close()

    # Para visualizar em que arquivo estava em caso de erro ou falha
    print(f"Arquivo: {file} - Contrato: {counter}")

f2.close()
driver.quit()
