"""
Módulo de configuração - carrega variáveis de ambiente
"""
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Nome do arquivo de saída
OUTPUT_FILENAME = 'Oferta_Relampago.xlsx'

# Caminho para o arquivo SQL
SQL_FILE = 'query.sql'
