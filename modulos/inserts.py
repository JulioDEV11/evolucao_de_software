import psycopg2
from datetime import datetime
import config

dbConfig = config.DB_CONFIG
token = config.GITHUB_TOKEN

def conectarBanco():
    try:
        return psycopg2.connect(**dbConfig)
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None
    
def inserirNoBanco(issues):
    conn = conectarBanco()
    if not conn:
        return

    try:
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

            prioridade = next((label.get("name") for label in issue.get("labels", []) if label), None)
            milestone = issue.get("milestone", {}).get("title", None) if isinstance(issue.get("milestone"), dict) else None
            autor = issue.get("user", {}).get("login", None) if isinstance(issue.get("user"), dict) else None
            atribuido = issue.get("assignee", {}).get("login", None) if isinstance(issue.get("assignee"), dict) else None

            cursor.execute(
                """
                INSERT INTO github_issues (issue_id, titulo, corpo, data_abertura, data_conclusao, 
                                          tempo_resolucao, prioridade, milestone, autor, 
                                          atribuido, tema_relacionado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (issue_id) DO NOTHING;
                """,
                (issue_id, title, body, created_at, closed_at, tempo_resolucao, prioridade or "", milestone or "", autor or "", atribuido or "", None)
            )

        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")
    finally:
        conn.close()