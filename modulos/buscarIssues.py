import requests
import random
import config

token = config.GITHUB_TOKEN
TAM = 300
Array = [
2183460626,
1396814237,
1395378869,
2190893314,
2190646571,
2190558248,
2189871931,
2189622944,
2181916905,
2188034467,
2186347678,
2185810948,
2185506208,
1998180711,
2182899381,
2183951960,
2183950926,
2183947799,
1401912870,
2183944879,
2182902731,
1402071632,
1402008116,
1402004146,
1401811549,
1401741035,
1401586423,
1401275044,
1401227201,
1401197864,
1401137537,
1401090028,
1401035512,
1400946520,
1400880116,
1400804548,
1400675878,
1400328613,
1400292931,
1400072442,
1399882497,
1399510172,
1398435256,
1398411070,
1398235872,
1397720690,
1396991316,
1991689419,
1396852060,
1396738823,
1396737681,
1396675353,
1396552712,
1396464972,
1396280941,
1396264445,
1395911746,
1395458517,
1395216499,
1395039774,
1394987812,
1394568589,
1394515117,
1393690175,
1999271531,
1998613551,
1998243839,
1998196756,
1996389738,
1995936241,
1995351618,
1994344901,
1994199645,
1993830213,
1993282749,
1992292952,
1991655286,
1991468598]

def buscarIssues(): #essa função faz a busca das issues de forma randomica, variando entre as paginas para que haja uma maior variedade entre issues mais novas e antigas.
    issues = []
    max_pages = 200
    paginas_aleatorias = random.sample(range(1, max_pages + 1), 15)

    for page in Array:
    
        url = f"https://api.github.com/repos/Vercel/next.js/issues/{page}"
        
        headers = {"Authorization": f"token {token}"}
        params = {"state": "closed", "per_page": 100}

        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            issues.extend(response.json())
        else:
            raise Exception(f"Erro ao acessar API: {response.status_code} - {response.text}")
    return issues[:TAM]