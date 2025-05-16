import requests
import pandas as pd
import time

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

def obter_proposicoes(ano, sigla_tipo="PL", max_paginas=5):
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

        resposta = requests.get(BASE_URL, params=params, headers=headers)
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

        time.sleep(1)  # evitar sobrecarga na API

    return lista_proposicoes

def salvar_em_excel(lista, nome_arquivo):
    df = pd.DataFrame(lista)
    df.to_excel(nome_arquivo, index=False)
    print(f"Arquivo salvo como: {nome_arquivo}")

def main():
    ano = 2024
    tipo = "PL"  # Projeto de Lei
    proposicoes = obter_proposicoes(ano=ano, sigla_tipo=tipo, max_paginas=10)
    salvar_em_excel(proposicoes, f"projetos_{tipo}_{ano}.xlsx")

if __name__ == "__main__":
    main()
