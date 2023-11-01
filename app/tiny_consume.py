# Importando bibliotecas
import requests
import json
import pandas as pd
import time
import os
from datetime import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

TINY_TOKEN = os.getenv("TINY_TOKEN")
HOST = os.getenv("HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Informações de conexão com o banco de dados PostgreSQL
db_config = {
    "host": 'localhost',
    "database": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}


pd.set_option('display.max_columns', None)

# Registra o tempo antes da execução
start_prog = time.time()

# Configurações da API Tiny

token = TINY_TOKEN
formato = 'JSON'