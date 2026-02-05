"""
Script principal - Gerador de Planilha Oferta Relâmpago
Extrai dados do PostgreSQL e gera planilha Excel formatada
"""
import os
import sys
from database import DatabaseConnection
from export_excel import ExcelExporter
from config import OUTPUT_FILENAME, SQL_FILE


def load_sql_query(sql_file: str) -> str:
    """
    Carrega a query SQL do arquivo
    
    Args:
        sql_file: Caminho do arquivo SQL
        
    Returns:
        String com a query SQL
    """
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            query = f.read()
        return query
    except FileNotFoundError:
        print(f"❌ Arquivo {sql_file} não encontrado!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo SQL: {e}")
        sys.exit(1)


def main():
    """Função principal do script"""
    print("=" * 60)
    print("🚀 GERADOR DE PLANILHA OFERTA RELÂMPAGO")
    print("=" * 60)
    print()
    
    # Carrega a query SQL
    query = load_sql_query(SQL_FILE)
    
    # Conecta ao banco e executa query
    with DatabaseConnection() as db:
        if not db.connection:
            print("❌ Não foi possível conectar ao banco de dados.")
            print("💡 Verifique suas credenciais no arquivo .env")
            sys.exit(1)
        
        # Executa a query
        df = db.execute_query(query)
        
        if df is None or df.empty:
            print("⚠️ Nenhum dado foi retornado pela query.")
            sys.exit(1)
    
    # Exporta para Excel
    success = ExcelExporter.export_data(df, OUTPUT_FILENAME)
    
    if success:
        file_path = os.path.abspath(OUTPUT_FILENAME)
        print()
        print("=" * 60)
        print(f"✅ SUCESSO! Arquivo gerado:")
        print(f"📁 {file_path}")
        print("=" * 60)
    else:
        print("❌ Falha ao gerar planilha.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
