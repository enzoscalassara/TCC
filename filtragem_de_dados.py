# Dados iniciais retirados de www.usaspending.gov
# Dados referentes aos contratos emitidos no ano fiscal de 2018
import os
import pandas as pd
import re

# Pasta contendo todos os dados, separados em 6 arquivos diferentes
data_directory = "Dados"

i = 1

names_list = []

# Loop para acessar todos os arquivos dentro da pasta de dados

for file in os.listdir(data_directory):
    file_path = os.path.join(data_directory, file)

    # Lendo o arquivo como DataFrame do pandas, para uma manipulação mais fácil
    file1 = pd.read_csv(filepath_or_buffer=file_path, low_memory=False, on_bad_lines='warn')

    # Selecionando apenas as colunas relevantes para o escopo do projeto
    file_filtered = file1['awarding_agency_name', 'action_date', 'total_dollars_obligated', 'recipient_name_raw']


    # Selecionando apenas contratos emitidos pela NASA e DoD
    file_filtered = file_filtered.loc[(file_filtered['awarding_agency_name'] == 'Department of Defense') |
                                      (file_filtered['awarding_agency_name'] == 'National Aeronautics and Space Administration')]

    # Selecionando apenas contratos com valor superior a 100k dólares
    file_filtered = file_filtered.loc[(file_filtered['total_dollars_obligated'] > 100000.00)]

    # Juntando os nomes de todas as empresas nos contratos, para depois salvar em um novo arquivo
    names_list.append(pd.Series(file_filtered['recipient_name_raw']))


    # Salvando em novos arquivos .csv os dados filtrados
    file_filtered.to_csv(f"Dados-filtrados\\2018-{i}-filtered_columns.csv", index=False)
    i += 1

# Salvando os nomes de todas as empresas nos contratos espalhados entre 6 arquivos em um único arquivo .csv
pd.concat([name for name in names_list]).to_csv("Dados-filtrados\\company-names-merged.csv", index=False)


