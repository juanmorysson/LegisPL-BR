import requests
import pandas as pd
import time

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def obter_proposicoes(ano, sigla_tipo="PL"):
    lista_proposicoes = []
    headers = {"accept": "application/json"}
    pagina = 1

    while True:
        print(f"Ano {ano} - Página {pagina}")
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
                "ementa": item["ementa"]
            })

        pagina += 1
        time.sleep(1)

    return lista_proposicoes

def obter_autores(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}/autores"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return {"autores": "Erro", "tipo_autor": "Erro"}

        autores = resp.json()["dados"]
        nomes = [
            f"{a['nome']} ({a.get('partido','?')}-{a.get('uf','?')})"
            for a in autores if a.get("nome")
        ]
        tipos = list(set(a.get("tipo", "") for a in autores if a.get("tipo")))
        tipo_autor = ", ".join(tipos) if tipos else "Não especificado"
        return {
            "autores": ", ".join(nomes) if nomes else "Sem autor registrado",
            "tipo_autor": tipo_autor
        }
    except Exception as e:
        return {"autores": f"Erro: {e}", "tipo_autor": "Erro"}

def obter_tramitacao(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}/tramitacoes"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return {
                "orgao_inicial": "Erro", "descricao_inicial": "Erro", "data_inicial": "Erro",
                "orgao_ultimo": "Erro", "descricao_ultimo": "Erro", "data_ultimo": "Erro"
            }

        dados = resp.json()["dados"]
        if not dados:
            return {
                "orgao_inicial": "Sem tramitação", "descricao_inicial": "", "data_inicial": "",
                "orgao_ultimo": "", "descricao_ultimo": "", "data_ultimo": ""
            }

        primeira = dados[0]
        ultima = dados[-1]

        return {
            "orgao_inicial": primeira.get("orgao", {}).get("nome", ""),
            "descricao_inicial": primeira.get("descricaoTramitacao", ""),
            "data_inicial": primeira.get("dataHora", "")[:10],
            "orgao_ultimo": ultima.get("orgao", {}).get("nome", ""),
            "descricao_ultimo": ultima.get("descricaoTramitacao", ""),
            "data_ultimo": ultima.get("dataHora", "")[:10],
        }
    except Exception as e:
        return {
            "orgao_inicial": f"Erro: {e}", "descricao_inicial": "", "data_inicial": "",
            "orgao_ultimo": "", "descricao_ultimo": "", "data_ultimo": ""
        }

def obter_status_proposicao(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return "Erro"
        dados = resp.json()["dados"]
        return dados.get("statusProposicao", {}).get("descricaoSituacao", "Indefinido")
    except Exception as e:
        return f"Erro: {e}"

def obter_keywords(id_proposicao):
    url = f"{BASE_URL}/proposicoes/{id_proposicao}/temas"
    try:
        resp = requests.get(url, headers={"accept": "application/json"})
        if resp.status_code != 200:
            return "Erro"
        temas = resp.json()["dados"]
        return ", ".join(t['nome'] for t in temas if "nome" in t) or "Sem temas"
    except Exception as e:
        return f"Erro: {e}"

def main():
    anos = [2022, 2023, 2024]
    tipo = "PL"
    todas_proposicoes = []

    for ano in anos:
        print(f"\nColetando proposições do ano {ano}...\n")
        proposicoes = obter_proposicoes(ano=ano, sigla_tipo=tipo)

        print(f"\nBuscando autores, tramitações, status e temas para {len(proposicoes)} proposições de {ano}...\n")
        for prop in proposicoes:
            print(f"ID {prop['id']}...")

            autor_info = obter_autores(prop["id"])
            prop["autores"] = autor_info["autores"]
            prop["tipo de autor"] = autor_info["tipo_autor"]

            tram = obter_tramitacao(prop["id"])
            prop["órgão inicial"] = tram["orgao_inicial"]
            prop["descrição inicial"] = tram["descricao_inicial"]
            prop["data da apresentação"] = tram["data_inicial"]
            prop["último órgão"] = tram["orgao_ultimo"]
            prop["última tramitação"] = tram["descricao_ultimo"]
            prop["data da última tramitação"] = tram["data_ultimo"]

            prop["status atual"] = obter_status_proposicao(prop["id"])
            prop["temas"] = obter_keywords(prop["id"])

            time.sleep(0.5)

        todas_proposicoes.extend(proposicoes)

    df = pd.DataFrame(todas_proposicoes)
    df.to_excel(f"projetos_{tipo}_2022_2024_completo.xlsx", index=False)
    print("Arquivo salvo como 'projetos_PL_2022_2024_completo.xlsx'")

if __name__ == "__main__":
    main()