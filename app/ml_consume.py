# Importando bibliotecas
import json
import os
import time
from datetime import datetime

import pandas as pd
import psycopg2
import requests
from dotenv import load_dotenv
from loguru import logger
from pandas import json_normalize
from psycopg2 import sql
from utils import save_json_list_to_txt, sendREST

logger.add(
    "Data/Output/Log/ml_log.log",
    rotation="10 MB",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
SCRET_KEY = os.getenv("SCRET_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
HOST = os.getenv("HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# Informações de conexão com o banco de dados PostgreSQL
db_config = {
    "host": "localhost",
    "database": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}


class MeLiLoader:
    def __init__(self, db_config, ACCESS_TOKEN):
        self.db_config = db_config
        self.ACCESS_TOKEN = ACCESS_TOKEN

    def load_ml_inventory_id(self):
        logger.info(
            f"Buscando Inventory IDs de Produtos FulFillment na API do Mercado Livre"
        )
        try:
            conn = psycopg2.connect(
                **self.db_config
            )  # Conecta ao banco de dados usando db_config
            query = "SELECT * FROM tiny_ml_codes;"
            df_tiny_id = pd.read_sql_query(query, conn)
            conn.close()
            logger.info(f"Criando DataFrame com a tabela 'tiny_ml_codes'")
            return df_tiny_id
        except Exception as e:
            logger.info(f"Ocorreu um erro: {str(e)}")
            return None

    def get_fulfillment_json_list(self):
        logger.info("Buscando inventory_ids para consultar no Mercado Livre")

        df_codes = self.load_ml_inventory_id()

        df_codes = df_codes.head(10)

        counter = 0
        json_list = []

        for item in df_codes["ml_inventory_id"]:
            url = f"https://api.mercadolibre.com/inventories/{item}/stock/fulfillment"

            payload = {}
            headers = {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}
            logger.info(f"Buscando dados de: {item}")

            response = requests.get(url, headers=headers, data=payload)
            response_data = response.json()

            json_list.append(response_data)

            counter += 1

            if counter % 50 == 0:
                logger.info(f"Fazendo uma pausa de 1 minuto...")
                time.sleep(60)

        return json_list

    def get_fulfillment(self):
        logger.info("Buscando inventory_ids para consultar no Mercado Livre")

        json_list = self.get_fulfillment_json_list()

        output_file = "ml_fulfillment.txt"

        save_json_list_to_txt(json_list, output_file)

        df_er = json_normalize(
            json_list,
            record_path="external_references",
            meta=[
                "inventory_id",
                "total",
                "available_quantity",
                "not_available_quantity",
                "not_available_detail",
            ],
        )
        df_nad = json_normalize(
            json_list,
            record_path="not_available_detail",
            meta=[
                "inventory_id",
                "total",
                "available_quantity",
                "not_available_quantity",
                "external_references",
            ],
        )

        df_nad = df_nad.drop(columns="external_references")
        df_er = df_er.drop(columns="not_available_detail")

        common_cols = [
            "inventory_id",
            "total",
            "available_quantity",
            "not_available_quantity",
        ]

        df_fulfillment = df_er.merge(df_nad, on=common_cols, how="left")

        # map_cols = {'inventory_id': 'ml_inventory_id', 'id': 'ml_item_id', 'status': 'nad_status','quantity':'nad_quantity'}
        # df_fulfillment = df_fulfillment.rename(columns=map_cols)
        # order_col = ['ml_inventory_id','ml_item_id','variation_id','nad_status','nad_quantity','total','available_quantity','not_available_quantity','type']
        # df_fulfillment = df_fulfillment[order_col]

        # df_fulfillment['variation_id'] = df_fulfillment['variation_id'].astype(str)
        # df_fulfillment['nad_quantity'] = df_fulfillment['nad_quantity'].fillna(0).astype(int)

        return df_fulfillment

    def insert_fulfillment_db(self, df_fulfillment):
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        # Itere pelas linhas do DataFrame e insira os dados na tabela
        for index, row in df_fulfillment.iterrows():
            insert_query = sql.SQL(
                """
                INSERT INTO ml_fulfillment (ml_inventory_id, ml_item_id, variation_id, nad_status, nad_quantity, total, available_quantity, not_available_quantity, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            )
            cursor.execute(
                insert_query,
                (
                    row["ml_inventory_id"],
                    row["ml_item_id"],
                    row["variation_id"],
                    row["nad_status"],
                    row["nad_quantity"],
                    row["total"],
                    row["available_quantity"],
                    row["not_available_quantity"],
                    row["type"],
                ),
            )

        # Confirme as alterações
        conn.commit()

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()

        logger.info("Dados inseridos com sucesso na tabela 'ml_fulfillment5'!")

    def insert_fulfillment_history_db(self, df_fulfillment):
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        # Itere pelas linhas do DataFrame e insira os dados na tabela
        for index, row in df_fulfillment.iterrows():
            insert_query = sql.SQL(
                """
                INSERT INTO ml_fulfillment (ml_inventory_id, ml_item_id, variation_id, nad_status, nad_quantity, total, available_quantity, not_available_quantity, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            )
            cursor.execute(
                insert_query,
                (
                    row["ml_inventory_id"],
                    row["ml_item_id"],
                    row["variation_id"],
                    row["nad_status"],
                    row["nad_quantity"],
                    row["total"],
                    row["available_quantity"],
                    row["not_available_quantity"],
                    row["type"],
                ),
            )

        # Confirme as alterações
        conn.commit()

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()

        logger.info("Dados inseridos com sucesso na tabela 'ml_fulfillment5'!")


if __name__ == "__main__":
    start_prog = time.time()  # Registra o inicio da aplicação

    loader = MeLiLoader(db_config, ACCESS_TOKEN)
    df_fulfillment = loader.get_fulfillment()
    loader.insert_fulfillment_db(df_fulfillment)

    print(df_fulfillment)

    end_prog = time.time()  # Registra o tempo depois de toda aplicação
    elapsed_time = end_prog - start_prog  # Calcula o tempo decorrido
    logger.info(f"Tempo Total do processo: {elapsed_time / 60} minutos")
