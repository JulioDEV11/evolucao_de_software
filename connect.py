import requests
import csv
import psycopg2
import config

dbConfig = config.DB_CONFIG
arquivoCSV = "issues.csv"
token = config.GITHUB_TOKEN

"""
def buscarIssues():
    url = "https://api.github.com/repos/Vercel/next.js/issues"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception (f"Erro ao acessar API: {response.status_code} - {response.text}")
""" 
def connectPostgres():
    try:
        conn = psycopg2.connect(**dbConfig)
        print("Conexão estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
if __name__ == "__main__":  #teste de conexao com o banco
    conn = connectPostgres()
    if conn:
        conn.close()
        print("Conexão fechada.")