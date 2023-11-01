import datetime
import json
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv
from loguru import logger

logger.add(
    "tiny_log.log",
    rotation="10 MB",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)


load_dotenv()

token = os.getenv("TINY_TOKEN")
formato = "JSON"


def get_excel_tiny_ids(excel_path, sheet_name, column):
    try:
        # Dataframe com os IDs de produtos a consultar
        df_tiny_id = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=[column])
        logger.info(
            f"Total de {df_tiny_id.shape[0]} dados carregados do arquivo {excel_path}"
        )

        count_nan = df_tiny_id[column].isna().sum()  # Qtd de valores NaN
        # Converte para números inteiros e substitui os não numéricos por NaN
        df_tiny_id[column] = pd.to_numeric(df_tiny_id[column], errors="coerce")
        df_tiny_id_no_nan = df_tiny_id.dropna(subset=[column])  # Remove valores NaN
        logger.info(f"Removendo Valores NaN. Total de {count_nan} valores removidos")

        count_dup = df_tiny_id_no_nan.duplicated().sum()  # Remove duplicatas
        df_tiny_id_no_dup = df_tiny_id_no_nan.drop_duplicates()
        logger.info(f"Removendo duplicatas. Total de {count_dup} duplicatas removidas")
        logger.info(
            f"Tamanho total da consulta a Tiny API = {df_tiny_id_no_dup.shape[0]}"
        )

        # # Gera um CSV com IDs da Tiny sem duplicatas ou NaN
        # caminho_saida_csv = os.path.join('Data', 'New', 'tiny_id_no_dup.csv')
        # df_tiny_id_no_dup.to_csv(caminho_saida_csv, index=False)
        # logger.info(f'Arquivo "tiny_id_no_dup.csv" criado com sucesso em: {caminho_saida_csv}')

        return df_tiny_id_no_dup

    except Exception as e:
        logger.error(f"Erro ao carregar dados de arquivo: {e}")
        return None


def enviarREST(url, data, optional_headers=None):
    # - url: a URL para a qual a solicitação será enviada.
    # - data: os dados que serão enviados na solicitação.
    # - optional_headers: cabeçalhos opcionais que podem ser fornecidos. Se não fornecidos, assume-se um dicionário vazio.

    # Verifica se optional_headers não é None e atribua um dicionário vazio, se necessário.
    headers = optional_headers if optional_headers is not None else {}
    logger.info("Verificando headers")

    # Envia uma solicitação POST para a URL especificada com os dados e cabeçalhos fornecidos.
    response = requests.post(url, data=data, headers=headers)
    logger.info("Enviando requisição POST")

    # Se o status da resposta não é 200 (OK).
    if response.status_code != 200:
        # Lança uma exceção com mensagem de erro.
        msg = f"Problema com {url}, Status Code: {response.status_code}"
        raise Exception(logger.error(msg))

    logger.info("Requisição realizada com sucesso!")
    # Retorna o conteúdo da resposta como texto.
    return response.text


def get_tiny_stock(df_tiny_id, token, formato):
    df_tiny_id = df_tiny_id.head(3)

    url = "https://api.tiny.com.br/api2/produto.obter.estoque.php"
    reponses = []  # Lista para armazenar os resultados
    num = 0

    for id in df_tiny_id["ID Tiny"]:
        logger.info(f"Buscando dados de {id}")
        num += 1
        logger.info(f"Loop: {num}")
        data = {"token": token, "id": id, "formato": formato}
        reponse = enviarREST(url, data)
        reponses.append(reponse)

        # Verifica se é múltiplo de 50 para aguardar 1 minuto a cada 50 requisições
        if num % 50 == 0:
            logger.info("Esperando 1 minuto...")
            time.sleep(60)  # Pausa por 1 minuto

    return reponses


def process_json_list(json_list):
    logger.info(f"Processando {json_list}.")
    tiny_stock_df = pd.DataFrame()  # Inicializa DataFrame vazio

    # Processar cada JSON na lista
    for json_str in json_list:
        logger.info("Carregando lista Json")
        json_data = json.loads(json_str)  # Transforma string JSON em objeto Python

        # Extrair a parte "produto" do JSON
        logger.info("Extraindo dados dos produtos da lista Json")
        produto = json_data["retorno"]["produto"]
        depositos = produto["depositos"]

        # Verifica se lista de depósitos está presente
        logger.info("Extraindo dados de depósitos")
        if depositos:
            # Cria DataFrame temporário a partir da lista de depósitos
            temp_df = pd.json_normalize(depositos)

            # Adiciona colunas do nível "produto" ao DataFrame temporário
            for key, value in produto.items():
                temp_df[key] = value

            # Concatena DataFrame temporário ao DataFrame principal
            logger.info("Construindo DataFrame de Estoque")
            tiny_stock_df = pd.concat([tiny_stock_df, temp_df], ignore_index=True)

    # Reordena colunas
    col_order = [
        "id",
        "nome",
        "codigo",
        "unidade",
        "saldo",
        "saldoReservado",
        "deposito.nome",
        "deposito.desconsiderar",
        "deposito.saldo",
        "deposito.empresa",
    ]

    tiny_stock_df = tiny_stock_df[col_order]

    logger.info("Dataframe construido!")
    return tiny_stock_df


def save_responses(reponses, output_txt_path):
    try:
        # Escreve cada elemento da lista em uma linha do arquivo
        with open(output_txt_path, "w") as file:
            for response in reponses:
                file.write(response + "\n")
        logger.info(f"Os dados foram gravados no arquivo: {output_txt_path}")

    except Exception as e:
        logger.error(
            f"Erro ao armazenar resposta da requisição em {output_txt_path}: {e}"
        )


def save_tiny_stock(reponses, output_csv_path):
    try:
        df_tiny_stock = process_json_list(reponses)  # Cria DataFrame de Estoque da Tiny

        # Salva o DataFrame em um arquivo CSV
        logger.info(f"Criando arquivo {output_csv_path}")
        df_tiny_stock.to_csv(output_csv_path, index=False)
        logger.info(f"{output_csv_path} criado com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao construir df_tiny_stock: {e}")


def save_csv_df(df, path):
    df.to_csv(path, index=False)
    logger.info(f"DataFrame salvos como CSV em {path}")


def main():
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Caminho dos arquivos
    excel_path = r"Data\Base\Envios Full.xlsx"
    output_txt_path = f"Data/Output/responses_{date}.txt"
    output_csv_path = f"Data/Output/tiny_stock_{date}.csv"

    sheet_name = "Relação Full x Tiny"  # Nome da planilha

    column = "ID Tiny"  # Nome da coluna a carregar

    df_tiny_ids = get_excel_tiny_ids(excel_path, sheet_name, column)

    reponses = get_tiny_stock(df_tiny_ids, token, formato)

    save_responses(reponses, output_txt_path)

    save_tiny_stock(reponses, output_csv_path)


if __name__ == "__main__":
    start_prog = time.time()  # Registra o inicio da aplicação

    main()

    end_prog = time.time()  # Registra o tempo depois de toda aplicação
    elapsed_time = end_prog - start_prog  # Calcula o tempo decorrido
    logger.info(f"Tempo Total do processo: {elapsed_time / 60} minutos")
