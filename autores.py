import requests
import pandas as pd
import time

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def obter_proposicoes(ano, sigla_tipo="PL", max_paginas=3):
    lista_proposicoes = []
    headers = {"accept": "application/json"}

    for pagina in range(1, max_paginas + 1):
        print(f"Página {pagina}...")
        params = {
            "ano": ano,
            "siglaTipo": sigla_tipo,
            "itens": 100,
            "ordem": "DESC",
            "ordenarPor": "id",
            "pagina": pagina
        }

        resposta = requests.get(f"{BASE_URL}/proposicoes", params=params, headers=headers)
        if resposta.status_code != 200:
            print("Erro na requisição:", resposta.status_code)
            break

        dados = resposta.json()["dados"]
        if not dados:
            break

        for item in dados:
            lista_proposicoes.append({
                "id": item["id"],
                "tipo": item["siglaTipo"],
                "numero": item["numero"],
                "ano": item["ano"],
                "ementa": item["ementa"],
                #"dataApresentacao": item["dataApresentacao"]
            })

        time.sleep(1)  # evitar sobrecarga

    return lista_proposicoes

def obter_autores(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}/autores"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return "Erro"
        autores = resp.json()["dados"]
        nomes = [a["nome"] for a in autores]
        return ", ".join(nomes) if nomes else "Sem autor registrado"
    except Exception as e:
        return f"Erro: {e}"

def main():
    ano = 2024
    tipo = "PL"
    proposicoes = obter_proposicoes(ano=ano, sigla_tipo=tipo, max_paginas=5)

    print("Buscando autores...")
    for prop in proposicoes:
        print(f"ID {prop['id']}...")
        prop["autores"] = obter_autores(prop["id"])
        time.sleep(0.5)

    df = pd.DataFrame(proposicoes)
    df.to_excel(f"projetos_{tipo}_{ano}_com_autores.xlsx", index=False)
    print("Arquivo salvo com autores incluídos.")

if __name__ == "__main__":
    main()
