import pandas as pd
from datetime import datetime

# ===============================
# FUNÇÕES DE TRANSFORMAÇÃO
# ===============================

def foi_finalizado(status):
    finais = [
        "Arquivada", "Transformada em norma jurídica", "Rejeitada",
        "Retirada", "Declarada prejudicada", "Encerrada"
    ]
    if pd.isna(status):
        return False
    return any(p.lower() in status.lower() for p in finais)

def foi_aprovado(status):
    termos = ["transformada em norma", "transformado em lei", "promulgado", "sanção"]
    if pd.isna(status):
        return False
    return any(t in status.lower() for t in termos)

mapa_temas = {
    "saúde": "Saúde",
    "vacinação": "Saúde",
    "educação": "Educação",
    "ensino": "Educação",
    "meio ambiente": "Meio Ambiente",
    "ambiental": "Meio Ambiente",
    "imposto": "Economia",
    "tributação": "Economia",
    "financiamento": "Economia",
    "trabalho": "Direitos Humanos",
    "mulher": "Direitos Humanos",
    "violência": "Segurança Pública",
    "segurança": "Segurança Pública",
    "crime": "Segurança Pública",
}

def mapear_categoria_tema(temas):
    if pd.isna(temas):
        return "Indefinido"
    temas = temas.lower()
    for chave, categoria in mapa_temas.items():
        if chave in temas:
            return categoria
    return "Outro"

uf_para_regiao = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste", "PB": "Nordeste",
    "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul"
}

def extrair_uf_principal(autores_str):
    if pd.isna(autores_str):
        return None
    try:
        ufs = [a.strip().split("-")[-1].replace(")", "").strip() for a in autores_str.split("),") if "-" in a]
        if ufs:
            return ufs[0]
    except:
        return None
    return None

def mapear_regiao(uf):
    return uf_para_regiao.get(uf, "Indefinida")

# Mapeamento político
partido_para_bloco = {
    "PT": "Esquerda", "PSOL": "Esquerda", "PCdoB": "Esquerda", "REDE": "Esquerda",
    "PSB": "Esquerda", "PDT": "Esquerda", "PV": "Esquerda",
    "MDB": "Centrão", "PSD": "Centrão", "PP": "Centrão", "PL": "Centrão",
    "Republicanos": "Centrão", "União Brasil": "Centrão", "Avante": "Centrão",
    "Podemos": "Centrão", "Solidariedade": "Centrão", "Patriota": "Centrão", "PROS": "Centrão",
    "Novo": "Direita", "PSC": "Direita", "DEM": "Direita", "PSL": "Direita", "PRTB": "Direita"
}

def extrair_partido_principal(autores_str):
    if pd.isna(autores_str):
        return None
    try:
        partidos = [a.split("(")[-1].split("-")[0].strip() for a in autores_str.split("),") if "(" in a and "-" in a]
        if partidos:
            return partidos[0]
    except:
        return None
    return None

def classificar_bloco_partidario(partido):
    return partido_para_bloco.get(partido, "Outros")

# ===============================
# TRANSFORMAÇÃO PRINCIPAL
# ===============================

df = pd.read_excel("projetos_PL_2022_2024_completo.xlsx")

df["finalizado"] = df["status atual"].apply(foi_finalizado)
df["aprovado"] = df["status atual"].apply(foi_aprovado)

df["dias_tramitacao"] = (
    pd.to_datetime(df["data da última tramitação"], errors="coerce") -
    pd.to_datetime(df["data da apresentação"], errors="coerce")
).dt.days

df["tema_dominante"] = df["temas"].apply(mapear_categoria_tema)

df["uf_principal"] = df["autores"].apply(extrair_uf_principal)
df["região"] = df["uf_principal"].apply(mapear_regiao)

df["partido_principal"] = df["autores"].apply(extrair_partido_principal)
df["bloco_partidario"] = df["partido_principal"].apply(classificar_bloco_partidario)

# --------------------------
# Análises adicionais
# --------------------------

# Verifica ementas duplicadas
df["apensada_ou_duplicada"] = df.duplicated(subset="ementa", keep=False)

# Verifica autoria coletiva (mais de um autor separado por vírgula)
df["autoria_coletiva"] = df["autores"].apply(lambda x: isinstance(x, str) and ("," in x))

# Estima a quantidade de tramitações intermediárias
def estimar_qtd_tramitacoes(row):
    if row["data da apresentação"] == row["data da última tramitação"]:
        return 1
    return 2

df["qtd_tramitacoes"] = df.apply(estimar_qtd_tramitacoes, axis=1)

# ===============================
# SALVAR
# ===============================

df.to_excel("projetos_PL_2022_2024_transformado.xlsx", index=False)
print("Arquivo salvo como 'projetos_PL_2022_2024_transformado.xlsx'")
