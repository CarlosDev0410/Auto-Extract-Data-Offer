"""
Módulo de conexão e consulta ao banco de dados PostgreSQL
"""
import psycopg2
import pandas as pd
from typing import Optional
from config import DB_CONFIG


class DatabaseConnection:
    """Gerencia a conexão com o banco de dados PostgreSQL"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Estabelece conexão com o banco de dados
        
        Returns:
            bool: True se conectou com sucesso, False caso contrário
        """
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("✅ Conexão com banco de dados estabelecida com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
            return False
    
    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """
        Executa uma query SQL e retorna os resultados como DataFrame
        
        Args:
            query: String com a query SQL
            
        Returns:
            DataFrame com os resultados ou None em caso de erro
        """
        try:
            print("🔍 Executando query...")
            df = pd.read_sql_query(query, self.connection)
            print(f"✅ Query executada! {len(df)} registros encontrados.")
            return df
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            return None
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Conexão com banco de dados fechada.")
    
    def __enter__(self):
        """Permite usar com 'with' statement"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha conexão automaticamente ao sair do 'with'"""
        self.close()
