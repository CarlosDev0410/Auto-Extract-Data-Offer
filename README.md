# Gerador de Planilha Oferta Relâmpago

Este projeto Python extrai dados de um banco PostgreSQL e gera uma planilha XLSX formatada.

![alt text](/assets/image.png)

## 📋 Requisitos

- Python 3.8 ou superior
- PostgreSQL (acesso ao banco de dados)

## 🚀 Instalação

1. Clone ou baixe este projeto
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as credenciais do banco de dados:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha com suas credenciais do PostgreSQL

4. Configure a query SQL:
   - Edite o arquivo `query.sql` com sua consulta

## 🎯 Como Usar

### Opção 1: Interface Gráfica (Recomendado)

Execute a interface desktop moderna:
```bash
python gui.py
```

Uma janela moderna será aberta com um botão para baixar a planilha. A interface mostra a data da última extração e feedback visual durante o processo.

### Opção 2: Linha de Comando

Execute o script principal:
```bash
python main.py
```

O arquivo `Oferta_Relampago.xlsx` será gerado no diretório atual.

## 📁 Estrutura do Projeto

```
tabela_oferta/
├── gui.py               # Interface gráfica desktop (RECOMENDADO)
├── main.py              # Script linha de comando
├── config.py            # Carregamento de configurações
├── database.py          # Conexão com banco de dados
├── export_excel.py      # Geração e formatação do Excel
├── query.sql            # Query SQL a ser executada
├── .env.example         # Exemplo de arquivo de configuração
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
```

## 🔐 Segurança

- Nunca commit o arquivo `.env` com suas credenciais reais
- O arquivo `.gitignore` já está configurado para isso
