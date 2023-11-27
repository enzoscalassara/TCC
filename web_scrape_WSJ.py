# Web scraper para coletar o nome de todas as empresas no mercado de ações, retirando os dados do site oficial do
# Wall Street Journal, o acesso foi feito em setembro de 2023 (os parâmetros podem ter mudado desde então)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()

# Configurei como headless para não abrir a janela do navegador durante o processo
options.add_argument('--headless')

# Configurei o tamanho da janela para ter certeza que os dados que o scraper estaria visualizando os dados no mesmo
# formato em que eu via quando retirei os paths
options.add_argument("--window-size=1920,1080")

# Arquivo onde serão armazenados os dados coletados
file = open("stock_market_company_names.txt", "a")

driver = webdriver.Chrome(options=options)

# Lista com todas as páginas que incluem empresas no mercado de ações, separadas em listas com o nome do path e o
# número de páginas dentro desse path
pages = [['0-9', 2], ['a', 37], ['b', 23], ['c', 33], ['d', 14], ['e', 17], ['f', 14], ['g', 19], ['h', 18], ['i', 15],
         ['j', 9], ['k', 13], ['l', 12], ['m', 23], ['n', 17], ['o', 9], ['p', 20], ['q', 3], ['r', 13], ['s', 45],
         ['t', 22], ['u', 6], ['v', 9], ['w', 9], ['x', 3], ['y', 4], ['z', 6], ['Other', 1]]


# Loop retirando os dados da tabela presente em cada página a partir do XPATH da mesma e depois escrevendo no arquivo
# esses dados resgatados (fazendo append na string)
for page in pages:
    for page_num in range(page[1]):

        driver.get(f"https://www.wsj.com/market-data/quotes/company-list/a-z/{page[0].upper()}/{page_num + 1}")

        all_names = driver.find_elements(By.XPATH, '/html/body/div[2]/section[1]/div/section/table/tbody')

        for elem in all_names:
            file.write(f"{elem.text}\n")

file.close()

driver.quit()
