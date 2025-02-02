import psycopg2
import config

dbConfig = config.DB_CONFIG

#Criação de dicionários para filtragem das issues
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

#Classificar caso existam palavras no corpo ou título da issue
def classificarTema():
    try:
        conn = psycopg2.connect(**dbConfig)
        cursor = conn.cursor()
        cursor.execute("SELECT issue_id, titulo, corpo FROM github_issues WHERE tema_relacionado IS NULL;")
        issues = cursor.fetchall()

        for issue_id, title, body in issues:
            temas = []
            texto = (title + " " + (body or "")).lower()

            if any(word in texto for word in palavras_refatoracao):
                temas.append("Refatoração")
            if any(word in texto for word in palavras_teste_regressao):
                temas.append("Testes de Regressão")

            if temas:
                temas_str = ", ".join(temas)
                cursor.execute("UPDATE github_issues SET tema_relacionado = %s WHERE issue_id = %s;", (temas_str, issue_id))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar as classificações: {e}")