import requests
import random
import config

token = config.GITHUB_TOKEN
TAM = 300

def buscarIssues(): #essa função faz a busca das issues de forma randomica, variando entre as paginas para que haja uma maior variedade entre issues mais novas e antigas.
    issues = []
    max_pages = 200
    paginas_aleatorias = random.sample(range(1, max_pages + 1), 15)

    for page in paginas_aleatorias:
        if len(issues) >= TAM:
            break

        url = "https://api.github.com/repos/Vercel/next.js/issues"
        headers = {"Authorization": f"token {token}"}
        params = {"state": "closed", "per_page": 100, "page": page}

        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            issues.extend(response.json())
        else:
            raise Exception(f"Erro ao acessar API: {response.status_code} - {response.text}")
    return issues[:TAM]