# Web scraper para resgatar dados historicos de market cap de empresas no mercado de ações por meio da página
# www.marketcaphistory.com

import datetime as dt
import pandas as pd
import ast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Recebe como parâmetros o símbolo da empresa no mercado de ações, que eu nomeei 'tag' e a data do contrato indetificada
# por 'date'
def check_marketcap(tag, date):

    # Como os dados de market cap não são separados mensalmente mas trimestralmente, é necessário fazer uma conversão
    # para o trimestre em que a data se encontra
    date = date.split('-')
    date[1] = int(date[1])

    if 7 < date[1] < 11:
        date[1] = 9

    elif 4 < date[1] < 8:
        date[1] = 6

    elif 1 < date[1] < 5:
        date[1] = 3

    else:
        date[1] = 1

    year = date[0]
    month = date[1]

    # Configurações do Selenium
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)

    driver.get(f'https://www.marketcaphistory.com/?symbol={tag}')

    table = driver.find_elements(By.XPATH, '/html/body/center/div[4]/div[2]/div[2]/table[1]/tbody/tr[2]/td/center/table/tbody/tr')

    # Retirando o dado de dentro da tabela presente na página
    for row in table:

        cells = row.find_elements(By.TAG_NAME, 'td')

        if str(cells[0].text)[5:] == str(year) and str(cells[0].text)[0] == str(month):

            driver.quit()

            return cells[1].text

