import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from collections import Counter

# Configurações iniciais
sns.set(style="whitegrid")
plt.rcParams["figure.dpi"] = 100

# Carregar o arquivo
file_path = "projetos_PL_2022_2024_transformado.xlsx"
df = pd.read_excel(file_path)

# Conversões de tipo
df["ano"] = pd.to_numeric(df["ano"], errors='coerce')
df["dias_tramitacao"] = pd.to_numeric(df["dias_tramitacao"], errors='coerce')
df["qtd_tramitacoes"] = pd.to_numeric(df["qtd_tramitacoes"], errors='coerce')

# Seleção de colunas numéricas
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# Estatísticas descritivas
print("Estatísticas descritivas:")
print(df[numeric_cols].describe())

# Matriz de correlação
def matriz_correlacao():
    correlation_matrix = df[numeric_cols].corr()
    return correlation_matrix

# 1. Histograma dos dias de tramitação
def histograma():
    plt.figure(figsize=(10, 5))
    sns.histplot(df["dias_tramitacao"].dropna(), bins=30, kde=True)
    plt.title("Distribuição dos Dias de Tramitação")
    plt.xlabel("Dias de Tramitação")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.show()

# 2. Distribuição de projetos aprovados
def distribuicao():
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(x="aprovado", data=df)
    plt.title("Distribuição de Projetos Aprovados")
    plt.xlabel("Aprovado")
    plt.ylabel("Contagem")
    # Adicionar rótulos de valor nas barras
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            x=p.get_x() + p.get_width() / 2,
            y=height + 1,
            s=f'{int(height)}',
            ha='center'
        )
    plt.tight_layout()
    plt.show()

def distribuicao_pie():
    counts = df["aprovado"].value_counts()
    labels = counts.index.astype(str)  # converter True/False para string se necessário
    sizes = counts.values

    # Criar gráfico de pizza
    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',  # formatação de porcentagem com uma casa decimal
        startangle=90,
        counterclock=False
    )
    plt.title("Proporção de Projetos Aprovados")
    plt.tight_layout()
    plt.show()

# 3. Boxplot de dias de tramitação por aprovação
def box_plot():
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="aprovado", y="dias_tramitacao", data=df)
    plt.title("Dias de Tramitação por Situação de Aprovação")
    plt.xlabel("Aprovado")
    plt.ylabel("Dias de Tramitação")
    plt.tight_layout()
    plt.show()

# 4. Heatmap da matriz de correlação
def matriz_correlacao_plot(correlation_matrix):
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação entre Variáveis Numéricas")
    plt.tight_layout()
    plt.show()

def apovados_partidos():
    df2 = df[df["partido_principal"] != "?"]
    aprovados = df2[df2["aprovado"] == True]

    # Contar aprovações por partido
    partido_counts = aprovados["partido_principal"].value_counts().sort_values(ascending=False)

    # Plotar gráfico de barras
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=partido_counts.index, y=partido_counts.values, palette="viridis")
    plt.title("Partidos com Maior Número de PLs Aprovados")
    plt.xlabel("Partido")
    plt.ylabel("Quantidade de PLs Aprovados")

    # Adicionar rótulos nas barras
    for i, v in enumerate(partido_counts.values):
        ax.text(i, v + 0.5, str(v), ha='center')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def extrair_ufs(autores_str):
    if pd.isna(autores_str):
        return None
    try:
        # Extrair todas as UFs
        ufs = [a.strip().split("-")[-1].replace(")", "").strip()
               for a in autores_str.split("),") if "-" in a]

        if ufs:
            # Remover duplicatas, se desejar, usando set(ufs)
            return ", ".join(ufs)
        else:
            return None
    except:
        return None

def listar_ufs(aprovados=False):
    df["ufs"] = df["autores"].apply(extrair_ufs)
    df2 = df[df["ufs"] != "?"]
    if aprovados:
        df2 = df2[df2["aprovado"] == True]
    lista_ufs = []
    for ufs in df2["ufs"].dropna():
        lista_ufs.extend([uf.strip() for uf in ufs.split(",")])
    #print(lista_ufs)
    return lista_ufs

def listar_ufs_rejeitadas():
    df["ufs"] = df["autores"].apply(extrair_ufs)
    df2 = df[df["ufs"] != "?"]
    df2 = df2[df2["aprovado"] == False]
    df2 = df2[df2["finalizado"] == True]
    lista_ufs = []
    for ufs in df2["ufs"].dropna():
        lista_ufs.extend([uf.strip() for uf in ufs.split(",")])
    #print(lista_ufs)
    return lista_ufs

def extrair_partidos(autores_str):
    if pd.isna(autores_str):
        return None
    try:
        partidos = [a.split("(")[-1].split("-")[0].strip() for a in autores_str.split("),") if "(" in a and "-" in a]
        if partidos:
            return ", ".join(partidos)
    except:
        return None
    return None

def listar_partidos(aprovados=False):
    df["partidos"] = df["autores"].apply(extrair_partidos)
    df2 = df[df["partidos"] != "?"]
    if aprovados:
        df2 = df2[df2["aprovado"] == True]
    lista_partidos = []
    for partidos in df2["partidos"].dropna():
        lista_partidos.extend([p.strip() for p in partidos.split(",")])
    #print(lista_partidos)
    return lista_partidos

def brasil_ufs(lista_ufs, cmap="Blues"):
    contagem_ufs = Counter(lista_ufs)
    print(contagem_ufs)
    ufs_df = pd.DataFrame.from_dict(contagem_ufs, orient='index', columns=['quantidade']).reset_index()
    ufs_df.columns = ['uf', 'quantidade']

    # Ler o shapefile dos estados brasileiros (direto da web)
    estados = gpd.read_file(
        'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson')

    # Mapear nomes dos estados para siglas
    estados["uf"] = estados["name"].apply(lambda x: {
        'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA', 'Ceará': 'CE',
        'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO', 'Maranhão': 'MA',
        'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG', 'Pará': 'PA',
        'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI', 'Rio de Janeiro': 'RJ',
        'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR',
        'Santa Catarina': 'SC', 'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO'
    }.get(x, None))

    # Unir dados com o mapa
    mapa = estados.merge(ufs_df, how="left", on="uf")
    mapa["quantidade"] = mapa["quantidade"].fillna(0)

    # Plotar o mapa
    plt.figure(figsize=(12, 8))
    mapa.plot(column='quantidade',
              cmap=cmap,
              linewidth=0.8,
              edgecolor='0.8',
              legend=True,
              )
    # Acessa a colorbar
    cbar = plt.gcf().axes[-1]  # A colorbar é geralmente o último eixo da figura

    # Ajusta o tamanho dos números (ticks) da colorbar
    cbar.tick_params(labelsize=24)

    # Ajusta o label (título) da colorbar
    #cbar.set_ylabel("População Estimada", fontsize=16)

    #plt.title('Distribuição de PL rejeitadas por UF', fontsize=16)
    plt.axis('off')
    plt.show()

def partidos_pl(lista_partidos):
    import matplotlib.patches as patches
    import matplotlib as mpl
    mapa_blocos = {
        "PT": "Esquerda", "PSOL": "Esquerda", "PCdoB": "Esquerda", "REDE": "Esquerda",
        "PSB": "Esquerda", "PDT": "Esquerda", "PV": "Esquerda",
        "MDB": "Centrão", "PSD": "Centrão", "PP": "Centrão", "PL": "Centrão",
        "REPUBLICANOS": "Direita", "UNIÃO": "Centrão", "AVANTE": "Centrão", "CIDADANIA": "Centrão",
        "PODE": "Centrão", "SOLIDARIEDADE": "Centrão", "PATRIOTA": "Centrão", "PROS": "Centrão", "PRD": "Centrão",
        "NOVO": "Direita", "PSC": "Direita", "DEM": "Direita", "PSL": "Direita",
        "PRTB": "Direita", "PTB": "Direita", "PSDB": "Direita",
    }

    # 🔥 Contagem dos partidos por bloco
    bloco_list = [mapa_blocos.get(p) for p in lista_partidos if mapa_blocos.get(p) is not None]
    contagem_blocos = Counter(bloco_list)

    # 🔥 Criar DataFrame base
    df = pd.DataFrame({
        'Bloco': ['Esquerda', 'Centrão', 'Direita'],
        'PosicaoX': [0, 1, 2],
        'PosicaoY': [0, 0, 0],
        'Quantidade': [
            contagem_blocos.get('Esquerda', 0),
            contagem_blocos.get('Centrão', 0),
            contagem_blocos.get('Direita', 0)
        ]
    })

    # 🔥 Configurar o colormap
    cmap = plt.get_cmap('Reds')
    norm = mpl.colors.Normalize(vmin=df['Quantidade'].min(), vmax=df['Quantidade'].max())

    # 🔥 Criar figura
    fig, ax = plt.subplots(figsize=(12, 4))

    # 🔥 Desenhar retângulos com cor proporcional
    for i, row in df.iterrows():
        color = cmap(norm(row['Quantidade']))
        rect = patches.Rectangle(
            (row['PosicaoX'] - 0.5, -0.5), 1, 1,
            linewidth=1, edgecolor='black', facecolor=color
        )
        ax.add_patch(rect)

        # 🔥 Adicionar rótulo no centro do retângulo
        ax.text(row['PosicaoX'], 0,
                f"{row['Bloco']}\n{row['Quantidade']} PLs",
                ha='center', va='center',
                fontsize=18, weight='bold', color='black')

    # 🔥 Ajustes do gráfico
    plt.xticks([0, 1, 2], ['', '', ''], fontsize=12)
    plt.yticks([])
    plt.xlim(-0.5, 2.5)
    plt.ylim(-0.5, 0.5)
    #plt.title("Mapa de Calor Conceitual por Espectro Político", fontsize=16)
    plt.box(False)
    plt.grid(False)

    # 🔥 Adicionar legenda de cores
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="vertical", fraction=0.03, pad=0.04)
    cbar.ax.tick_params(labelsize=22)

    #cbar.set_label('Quantidade de PLs Aprovadas')

    plt.show()


def listar_partidos_com_contagem():
    df["partidos"] = df["autores"].apply(extrair_partidos)

    # Filtrar partidos válidos
    df_filtrado = df[df["partidos"].notna() & (df["partidos"] != "?")]

    # Lista para armazenar os registros
    registros = []

    # Percorrer cada linha do dataframe
    for _, row in df_filtrado.iterrows():
        partidos = [p.strip() for p in row["partidos"].split(",")]
        for partido in partidos:
            registros.append({
                "partido": partido,
                "aprovado": row["aprovado"]
            })

    # Criar DataFrame auxiliar
    df_aux = pd.DataFrame(registros)

    # Agrupar para contar submetidos e aprovados
    resultado = df_aux.groupby("partido").agg(
        quantidade_submetido=("partido", "count"),
        quantidade_aprovado=("aprovado", "sum")
    ).reset_index()

    return resultado

def indice_aprocacao(dados):
    dfx = pd.DataFrame(dados)
    # 🔥 Mapeamento dos blocos políticos
    mapa_blocos = {
        "PT": "Esquerda", "PSOL": "Esquerda", "PCdoB": "Esquerda", "REDE": "Esquerda",
        "PSB": "Esquerda", "PDT": "Esquerda", "PV": "Esquerda",
        "MDB": "Centrão", "PSD": "Centrão", "PP": "Centrão", "PL": "Centrão",
        "REPUBLICANOS": "Direita", "UNIÃO": "Centrão", "AVANTE": "Centrão", "CIDADANIA": "Centrão",
        "PODE": "Centrão", "SOLIDARIEDADE": "Centrão", "PATRIOTA": "Centrão", "PROS": "Centrão", "PRD": "Centrão",
        "NOVO": "Direita", "PSC": "Direita", "DEM": "Direita", "PSL": "Direita",
        "PRTB": "Direita", "PTB": "Direita", "PSDB": "Direita",
    }

    # 🔥 Adicionar bloco político
    dfx['bloco'] = dfx['partido'].map(mapa_blocos)

    # 🔥 Calcular taxa de aprovação
    dfx['taxa_aprovacao'] = (dfx['quantidade_aprovado'] / dfx['quantidade_submetido']) * 100

    # 🔥 Definir cores por bloco
    cores = {'Esquerda': 'red', 'Centrão': 'blue', 'Direita': 'green'}
    dfx['cor'] = dfx['bloco'].map(cores)
    dfx = dfx.dropna()
    # 🔥 Ordenar pelo índice de aprovação
    dfx = dfx.sort_values(by='taxa_aprovacao', ascending=False)

    # 🔥 Plotar gráfico de barras
    plt.figure(figsize=(10, 6))
    bars = plt.bar(dfx['partido'], dfx['taxa_aprovacao'], color=dfx['cor'])

    # 🔥 Adicionar rótulos nas barras
    for bar in bars:
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, altura + 0.5,
                 f'{altura:.1f}%', ha='center', rotation=90, fontsize=16)

    #plt.title('Índice de Aprovação de PLs por Partido (%)')
    plt.xlabel('Partido')
    plt.ylabel('Taxa de Aprovação (%)')
    plt.ylim(0, max(dfx['taxa_aprovacao']) + 5)
    plt.xticks(rotation=90, fontsize=20)
    plt.yticks(fontsize=18)


    # 🔥 Adicionar legenda manual
    from matplotlib.patches import Patch
    legenda = [Patch(color='red', label='Esquerda'),
               Patch(color='blue', label='Centrão'),
               Patch(color='green', label='Direita')]
    plt.legend(handles=legenda, fontsize=20)

    plt.tight_layout()
    plt.show()

def indice_aprocacao_bloco(dados):
    dfx = pd.DataFrame(dados)
    # 🔥 Mapeamento dos blocos políticos
    # 🔥 Mapeamento dos blocos políticos
    mapa_blocos = {
        "PT": "Esquerda", "PSOL": "Esquerda", "PCdoB": "Esquerda", "REDE": "Esquerda",
        "PSB": "Esquerda", "PDT": "Esquerda", "PV": "Esquerda",
        "MDB": "Centrão", "PSD": "Centrão", "PP": "Centrão", "PL": "Centrão",
        "REPUBLICANOS": "Direita", "UNIÃO": "Centrão", "AVANTE": "Centrão", "CIDADANIA": "Centrão",
        "PODE": "Centrão", "SOLIDARIEDADE": "Centrão", "PATRIOTA": "Centrão", "PROS": "Centrão", "PRD": "Centrão",
        "NOVO": "Direita", "PSC": "Direita", "DEM": "Direita", "PSL": "Direita",
        "PRTB": "Direita", "PTB": "Direita", "PSDB": "Direita"
    }

    # 🔥 Adicionar bloco político
    dfx['bloco'] = dfx['partido'].map(mapa_blocos)

    # 🔥 Agrupar por bloco
    df_bloco = dfx.groupby('bloco').agg(
        quantidade_submetida=('quantidade_submetido', 'sum'),
        quantidade_aprovada=('quantidade_aprovado', 'sum')
    ).reset_index()

    # 🔥 Calcular taxa de aprovação
    df_bloco['taxa_aprovacao'] = (df_bloco['quantidade_aprovada'] / df_bloco['quantidade_submetida']) * 100

    # 🔥 Definir cores
    cores = {'Esquerda': 'red', 'Centrão': 'blue', 'Direita': 'green'}
    df_bloco['cor'] = df_bloco['bloco'].map(cores)

    # 🔥 Plotar gráfico
    plt.figure(figsize=(9, 3))
    bars = plt.bar(df_bloco['bloco'], df_bloco['taxa_aprovacao'], color=df_bloco['cor'])

    # 🔥 Adicionar rótulos nas barras
    for bar in bars:
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, altura + 0.5,
                 f'{altura:.1f}%', ha='center', fontsize=22)

    #plt.title('Índice de Aprovação de PLs por Espectro Político (%)')
    plt.xlabel('Espectro Político')
    plt.ylabel('Taxa de Aprovação (%)')
    plt.ylim(0, max(df_bloco['taxa_aprovacao']) + 5)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=18)

    plt.tight_layout()
    plt.show()

#indice_aprocacao_bloco(listar_partidos_com_contagem())
#indice_aprocacao(listar_partidos_com_contagem())
#partidos_pl(listar_partidos(True))
#brasil_ufs(listar_ufs_rejeitadas(), cmap="Reds") #rejeitados
#brasil_ufs(listar_ufs(True))
#brasil_ufs(listar_ufs())
#Counter({'SP': 3099, 'RJ': 1726, 'MG': 1172, 'RS': 1091, 'PR': 758, 'GO': 744, 'PE': 708, 'BA': 700, 'CE': 679, 'MA': 608, 'SC': 559, 'DF': 532, 'AM': 520, 'ES': 408, 'PA': 392, 'MT': 348, 'PB': 341, 'MS': 305, 'RO': 302, 'AL': 297, 'RR': 237, 'TO': 229, 'SE': 223, 'RN': 207, 'AP': 194, 'AC': 194, 'PI': 189})
#Counter({'SP': 40, 'RS': 29, 'RJ': 25, 'PE': 23, 'CE': 22, 'MG': 17, 'PR': 13, 'DF': 11, 'GO': 10, 'MA': 10, 'BA': 9, 'PB': 9, 'SC': 8, 'AL': 7, 'ES': 6, 'PA': 5, 'AC': 5, 'MS': 4, 'PI': 4, 'RO': 3, 'RN': 2, 'MT': 2, 'AM': 2, 'AP': 2, 'RR': 1, 'TO': 1, 'SE': 1})
#histograma()
#distribuicao_pie()
#apovados_partidos()
#distribuicao()
#box_plot()
#matriz_correlacao_plot(matriz_correlacao())

import matplotlib.pyplot as plt
import numpy as np

# Dados
labels = ['Esquerda', 'Centrão', 'Direita']
submetidas = [5107, 9910, 1741]
aprovadas = [112, 133, 26]

x = np.arange(len(labels))  # posições dos grupos
width = 0.35  # largura das barras

fig, ax = plt.subplots(figsize=(12, 6))

# Barras para submetidas (cores claras)
bars1 = ax.bar(x - width/2, submetidas, width, label='Submetidas',
               color=['lightcoral', 'lightblue', 'lightgreen'])

# Barras para aprovadas (cores escuras)
bars2 = ax.bar(x + width/2, aprovadas, width, label='Aprovadas',
               color=['darkred', 'darkblue', 'darkgreen'])

# Labels e título
ax.set_ylabel('Quantidade de PLs', fontsize=22)
#.set_title('Submissões e Aprovações de PLs por Espectro Político', fontsize=20)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=22)
#ax.legend(fontsize=12)

# Adiciona valores no topo das barras
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # deslocamento
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=24)

plt.tight_layout()
plt.show()
