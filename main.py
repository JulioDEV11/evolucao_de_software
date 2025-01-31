from modulos.buscarIssues import buscarIssues
from modulos.inserts import inserirNoBanco
from modulos.classificarIssues import classificarTema

def main():
    try:
        print("Conectando ao banco de dados...")

        issues = buscarIssues()
        print(f"{len(issues)} issues encontradas.")

        print("Inserindo no banco de dados...")
        inserirNoBanco(issues)

        print("Classificando e atualizando os dados...")
        classificarTema()

        print("Concluído! Encerrando conexao com o banco.")
    except Exception as e:
        print(f"Erro no processamento: {e}")

if __name__ == "__main__":
    main()
