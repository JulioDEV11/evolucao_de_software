import requests
import psycopg2
from datetime import datetime
import random
import config

dbConfig = config.DB_CONFIG
token = config.GITHUB_TOKEN
TAM = 500

def buscarIssues(): #essa função faz a busca das issues de forma randomica, variando entre as paginas para que haja uma maior variedade entre issues mais novas e antigas.
    issues = []
    max_pages = 200
    paginas_aleatorias = random.sample(range(1, max_pages + 1), 15)

    for page in paginas_aleatorias:
        if len(issues) >= TAM:
            break

        url = "https://api.github.com/repos/Vercel/next.js/issues"
        headers = {"Authorization": f"token {token}"}
        params = {"state": "closed", "labels": "bug", "per_page": 100, "page": page}

        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            issues.extend(response.json())
        else:
            raise Exception(f"Erro ao acessar API: {response.status_code} - {response.text}")
    return issues[:TAM]

def inserirNoBanco(issues): #essa função insere as informações das issues na tabela criada no postgres
    try:
        conn = psycopg2.connect(**dbConfig)
        cursor = conn.cursor()

        for issue in issues:
            if issue is None:
                continue

            issue_id = issue.get("id")
            if issue_id is None:
                continue

            title = issue.get("title", "")
            body = issue.get("body", "") or ""
            created_at = issue.get("created_at", None)
            closed_at = issue.get("closed_at", None)

            tempo_resolucao = None
            if created_at and closed_at:
                try:
                    created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                    closed_date = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
                    tempo_resolucao = (closed_date - created_date).days
                except ValueError:
                    continue

            prioridade = None
            labels = issue.get("labels", [])
            if isinstance(labels, list) and len(labels) > 0:
                prioridade = labels[0].get("name", None)

            milestone = None
            if isinstance(issue.get("milestone"), dict):
                milestone = issue.get("milestone", {}).get("title", None)

            autor = None
            if isinstance(issue.get("user"), dict):
                autor = issue.get("user", {}).get("login", None)

            atribuido = None
            if isinstance(issue.get("assignee"), dict):
                atribuido = issue.get("assignee", {}).get("login", None)

            tema_relacionado = None

            cursor.execute(
                """
                INSERT INTO github_issues (issue_id, titulo, corpo, data_abertura, data_conclusao, 
                                          tempo_resolucao, prioridade, milestone, autor, 
                                          atribuido, tema_relacionado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (issue_id) DO NOTHING;
                """,
                (issue_id, title, body, created_at, closed_at, tempo_resolucao, prioridade or "", milestone or "", autor or "", atribuido or "", tema_relacionado)
            )

        conn.commit()
        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")

def classificarTema():  #essa função verifica o titulo e o corpo da issue e procura por palavras-chave qeu estejam relacionadas com os temas ((i) Refatoração e (ii) Testes de regressão.) após isso ele as classifica
    try:
        conn = psycopg2.connect(**dbConfig)
        cursor = conn.cursor()
        cursor.execute("SELECT issue_id, titulo, corpo FROM github_issues WHERE tema_relacionado IS NULL;")
        issues = cursor.fetchall()

        for issue_id, title, body in issues:
            temas = []
            texto = (title + " " + (body or "")).lower()  # concatena e evita noneType

            palavras_refatoracao = [
                "refactor", "refactoring", "code cleanup", "optimize", "improve performance",
                "restructure", "reorganize", "simplify", "remove duplication", "enhance readability",
                "code optimization", "code improvement", "modularization", "reduce complexity", "design improvement", "redundant code", "legacy code cleanup",
                "maintainability", "clean code", "reengineering", "architecture improvement",
                "performance tuning", "best practices", "technical debt", "code standardization"
            ]

            palavras_teste_regressao = [
                "regression test", "regression testing", "bug fix", "stability test",
                "automated test", "unit test", "functional test", "qa test", "test suite", "test failure",
                "integration test", "acceptance test", "smoke test", "sanity test",
                "flaky test", "test automation", "test refactor", "mock test", "test validation",
                "code coverage", "test-driven development", "test reliability",
                "bug reproduction", "quality assurance", "software validation",
                "test execution", "edge case", "test case design", "regression issue"
            ]

            if any(word in texto for word in palavras_refatoracao):
                temas.append("Refatoração")

            if any(word in texto for word in palavras_teste_regressao):
                temas.append("Testes de regressão")

            if temas:
                temas_str = ", ".join(temas)
                cursor.execute("UPDATE github_issues SET tema_relacionado = %s WHERE issue_id = %s;", (temas_str, issue_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar as classificações: {e}")

def main():
    try:
        print("Conectando ao banco de dados...")

        issues = buscarIssues()
        print(f"{len(issues)} issues encontradas e processadas.")

        print("Inserindo no banco de dados...")
        inserirNoBanco(issues)

        print("Classificando e atualizando os dados...")
        classificarTema()

        print("Conexão com o banco encerrada.")
    except Exception as e:
        print(f"Erro: {e}")
    
if __name__ == "__main__":
    main()