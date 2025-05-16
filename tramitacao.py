import requests
import pandas as pd
import time

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def obter_proposicoes(ano, sigla_tipo="PL", max_paginas=300):
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

        time.sleep(1)

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

def obter_tramitacao(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}/tramitacoes"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return {"ultimo_orgao": "Erro", "ultimo_status": "Erro", "data_ultima": "Erro"}

        dados = resp.json()["dados"]
        if not dados:
            return {"ultimo_orgao": "Sem tramitação", "ultimo_status": "", "data_ultima": ""}

        ultima = dados[-1]  # último andamento
        return {
            "ultimo_orgao": ultima.get("orgao", {}).get("nome", ""),
            "ultimo_status": ultima.get("descricaoTramitacao", ""),
            "data_ultima": ultima.get("dataHora", "")[:10]
        }
    except Exception as e:
        return {"ultimo_orgao": f"Erro: {e}", "ultimo_status": "", "data_ultima": ""}

def main():
    anos = [2022, 2023, 2024]
    tipo = "PL"
    todas_proposicoes = []

    for ano in anos:
        proposicoes = obter_proposicoes(ano=ano, sigla_tipo=tipo)

        print(f"\n Buscando autores e tramitação para ano {ano}...\n")
        for prop in proposicoes:
            print(f"ID {prop['id']}...")
            prop["autores"] = obter_autores(prop["id"])
            tram = obter_tramitacao(prop["id"])
            prop["último órgão"] = tram["ultimo_orgao"]
            prop["última tramitação"] = tram["ultimo_status"]
            prop["data da última tramitação"] = tram["data_ultima"]
            time.sleep(0.5)

        todas_proposicoes.extend(proposicoes)

    df = pd.DataFrame(todas_proposicoes)
    df.to_excel(f"projetos_{tipo}_2022_2024_completo.xlsx", index=False)
    print("Arquivo salvo como 'projetos_PL_2022_2024_completo.xlsx'")

if __name__ == "__main__":
    main()
