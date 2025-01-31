# Evolução de Software

Este projeto automatiza a coleta, armazenamento e classificação de issues do repositório **Vercel/next.js** no GitHub. Ele extrai dados de issues fechadas, insere-os em um banco de dados PostgreSQL e categoriza os temas relacionados, focando em **Refatoração** e **Testes de Regressão**.

## 🚀 Funcionalidades

- **Coleta de Issues**: Busca issues fechadas aleatoriamente para maior diversidade.
- **Armazenamento no Banco**: Insere as informações relevantes no banco de dados.
- **Classificação de Temas**: Identifica palavras-chave para determinar se a issue se refere a **Refatoração** ou **Testes de Regressão**.

## 🛠️ Tecnologias Utilizadas

- **Python**: Automação e manipulação de dados.
- **Requests**: API do GitHub para coleta de issues.
- **PostgreSQL**: Banco de dados para armazenamento e consultas.
- **Psycopg2**: Conector para interação com PostgreSQL.

## 📂 Estrutura do Projeto

```
📦 evolucao_de_software
 ├── 📜 connect.py  # Código principal com a lógica de extração, armazenamento e classificação
 ├── 📜 config.py   # Configurações do banco de dados e token do GitHub (não incluído por segurança)
 ├── 📜 README.md   # Documentação do projeto
```

## 📌 Como Usar

1. **Configurar as Credenciais**:  
   - Crie um arquivo `config.py` contendo:  
     ```python
     DB_CONFIG = {
         "dbname": "seu_banco",
         "user": "seu_usuario",
         "password": "sua_senha",
         "host": "localhost",
         "port": "5432"
     }
     GITHUB_TOKEN = "seu_token_pessoal"
     ```

2. **Instalar Dependências**:  
   ```
   pip install requests psycopg2
   ```

3. **Executar o Script**:  
   ```
   python connect.py
   ```
