import pandas as pd
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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

mapa_temas_completo = {
    "Agricultura, Pecuária, Pesca e Extrativismo":"Economia",
    "Estrutura Fundiária":"Direitos Humanos",
    "Administração Pública":"Economia",
    "Viação, Transporte e Mobilidade":"Meio Ambiente",
    "Agricultura, Pecuária, Pesca e Extrativismo, Viação, Transporte e Mobilidade":"Meio Ambiente",
    "Cidades e Desenvolvimento Urbano, Viação, Transporte e Mobilidade":"Meio Ambiente",
    "Arte, Cultura e Religião, Comunicações":"Educação",
    "Arte, Cultura e Religião":"Educação",
    "Administração Pública, Cidades e Desenvolvimento Urbano":"Meio Ambiente",
    "Agricultura, Pecuária, Pesca e Extrativismo, Cidades e Desenvolvimento Urbano":"Meio Ambiente",
    "Administração Pública, Cidades e Desenvolvimento Urbano, Estrutura Fundiária":"Economia",
    "Administração Pública, Viação, Transporte e Mobilidade":"Meio Ambiente",
    "Administração Pública, Cidades e Desenvolvimento Urbano, Direitos Humanos e Minorias": "Direitos Humanos",
    "Administração Pública, Arte, Cultura e Religião, Finanças Públicas e Orçamento": "Economia",
    "Direitos Humanos e Minorias, Economia, Finanças Públicas e Orçamento": "Economia",
    "Direitos Humanos e Minorias, Finanças Públicas e Orçamento": "Economia",
    "Economia, Previdência e Assistência Social": "Saúde",
    "Direitos Humanos e Minorias, Viação, Transporte e Mobilidade": "Direitos Humanos",
    "Direito Civil e Processual Civil, Direitos Humanos e Minorias": "Direitos Humanos",
    "Energia, Recursos Hídricos e Minerais, Finanças Públicas e Orçamento": "Meio Ambiente",
    "Direito Civil e Processual Civil, Viação, Transporte e Mobilidade": "Segurança Pública",
    "Cidades e Desenvolvimento Urbano, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Direitos Humanos e Minorias, Economia, Previdência e Assistência Social": "Saúde",
    "Administração Pública, Direitos Humanos e Minorias, Previdência e Assistência Social": "Saúde",
    "Agricultura, Pecuária, Pesca e Extrativismo, Energia, Recursos Hídricos e Minerais, Finanças Públicas e Orçamento": "Meio Ambiente",
    "Direito Civil e Processual Civil, Direitos Humanos e Minorias, Viação, Transporte e Mobilidade": "Direitos Humanos",
    "Agricultura, Pecuária, Pesca e Extrativismo, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Agricultura, Pecuária, Pesca e Extrativismo, Finanças Públicas e Orçamento, Indústria, Comércio e Serviços": "Economia",
    "Cidades e Desenvolvimento Urbano, Direitos Humanos e Minorias": "Direitos Humanos",
    "Direitos Humanos e Minorias, Previdência e Assistência Social": "Saúde",
    "Direito Civil e Processual Civil, Direito Penal e Processual Penal, Direitos Humanos e Minorias": "Direitos Humanos",
    "Energia, Recursos Hídricos e Minerais, Finanças Públicas e Orçamento, Política, Partidos e Eleições": "Meio Ambiente",
    "Finanças Públicas e Orçamento, Viação, Transporte e Mobilidade": "Economia",
    "Administração Pública, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Economia, Finanças Públicas e Orçamento": "Economia",
    "Direito e Defesa do Consumidor, Viação, Transporte e Mobilidade": "Direitos Humanos",
    "Administração Pública, Cidades e Desenvolvimento Urbano, Finanças Públicas e Orçamento": "Economia",
    "Energia, Recursos Hídricos e Minerais, Viação, Transporte e Mobilidade": "Meio Ambiente",
    "Administração Pública, Direito Penal e Processual Penal": "Segurança Pública",
    "Administração Pública, Cidades e Desenvolvimento Urbano, Direito e Defesa do Consumidor, Viação, Transporte e Mobilidade": "Direitos Humanos",
    "Administração Pública, Direitos Humanos e Minorias, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Direito Penal e Processual Penal, Indústria, Comércio e Serviços": "Economia",
    "Arte, Cultura e Religião, Direitos Humanos e Minorias, Esporte e Lazer": "Direitos Humanos",
    "Direito e Justiça, Direito Penal e Processual Penal": "Segurança Pública",
    "Arte, Cultura e Religião, Finanças Públicas e Orçamento": "Economia",
    "Economia, Viação, Transporte e Mobilidade": "Economia",
    "Direito Penal e Processual Penal, Estrutura Fundiária": "Segurança Pública",
    "Ciência, Tecnologia e Inovação, Finanças Públicas e Orçamento": "Economia",
    "Direitos Humanos e Minorias, Energia, Recursos Hídricos e Minerais, Finanças Públicas e Orçamento": "Meio Ambiente",
    "Direito e Defesa do Consumidor": "Direitos Humanos",
    "Direito e Defesa do Consumidor, Direito Penal e Processual Penal": "Direitos Humanos",
    "Direito Civil e Processual Civil, Direitos Humanos e Minorias, Estrutura Fundiária": "Direitos Humanos",
    "Previdência e Assistência Social": "Saúde",
    "Direitos Humanos e Minorias, Esporte e Lazer, Indústria, Comércio e Serviços": "Economia",
    "Direito Civil e Processual Civil, Finanças Públicas e Orçamento": "Economia",
    "Ciência, Tecnologia e Inovação, Direito Penal e Processual Penal, Direitos Humanos e Minorias": "Direitos Humanos",
    "Comunicações, Direito e Justiça, Direito Penal e Processual Penal": "Segurança Pública",
    "Administração Pública, Direito Civil e Processual Civil, Estrutura Fundiária": "Segurança Pública",
    "Direitos Humanos e Minorias, Estrutura Fundiária": "Direitos Humanos",
    "Direito e Defesa do Consumidor, Direitos Humanos e Minorias, Economia": "Economia",
    "Direito e Defesa do Consumidor, Direitos Humanos e Minorias": "Direitos Humanos",
    "Administração Pública, Direito Penal e Processual Penal, Finanças Públicas e Orçamento": "Economia",
    "Direito Penal e Processual Penal, Viação, Transporte e Mobilidade": "Segurança Pública",
    "Economia, Finanças Públicas e Orçamento, Indústria, Comércio e Serviços": "Economia",
    "Direitos Humanos e Minorias, Indústria, Comércio e Serviços": "Economia",
    "Administração Pública, Direitos Humanos e Minorias": "Direitos Humanos",
    "Direito e Defesa do Consumidor, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Finanças Públicas e Orçamento, Indústria, Comércio e Serviços, Relações Internacionais e Comércio Exterior": "Economia",
    "Administração Pública, Direito Penal e Processual Penal, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Comunicações, Direito Penal e Processual Penal, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Administração Pública, Direitos Humanos e Minorias, Economia, Finanças Públicas e Orçamento": "Economia",
    "Administração Pública, Direito e Defesa do Consumidor, Energia, Recursos Hídricos e Minerais": "Meio Ambiente",
    "Cidades e Desenvolvimento Urbano, Energia, Recursos Hídricos e Minerais, Indústria, Comércio e Serviços": "Meio Ambiente",
    "Comunicações, Direito Penal e Processual Penal": "Segurança Pública",
    "Ciência, Tecnologia e Inovação, Indústria, Comércio e Serviços": "Economia",
    "Indústria, Comércio e Serviços, Viação, Transporte e Mobilidade": "Economia",
    "Direito Penal e Processual Penal, Energia, Recursos Hídricos e Minerais, Indústria, Comércio e Serviços": "Meio Ambiente",
    "Homenagens e Datas Comemorativas": "Homenagens",
    "Direito Penal e Processual Penal, Direitos Humanos e Minorias": "Segurança Pública",
    "Direito Penal e Processual Penal": "Segurança Pública",
    "Direito Penal e Processual Penal, Homenagens e Datas Comemorativas": "Segurança Pública",
    "Direito Penal e Processual Penal, Direitos Humanos e Minorias, Indústria, Comércio e Serviços": "Segurança Pública",
    "Direito Civil e Processual Civil": "Segurança Pública",
    "Direito Civil e Processual Civil, Economia": "Segurança Pública",
    "Administração Pública, Direito Civil e Processual Civil": "Segurança Pública",
    "Administração Pública, Direito e Justiça": "Segurança Pública",

    "Direitos Humanos e Minorias": "Direitos Humanos",
    "Direitos Humanos e Minorias, Homenagens e Datas Comemorativas": "Direitos Humanos",
    "Direitos Humanos e Minorias, Esporte e Lazer": "Direitos Humanos",
    "Direitos Humanos e Minorias, Finanças Públicas e Orçamento, Previdência e Assistência Social": "Saúde",
    "Direitos Humanos e Minorias, Economia, Finanças Públicas e Orçamento, Previdência e Assistência Social": "Saúde",
    "Administração Pública, Finanças Públicas e Orçamento, Previdência e Assistência Social": "Saúde",

    "Energia, Recursos Hídricos e Minerais": "Meio Ambiente",

    "Economia": "Economia",
    "Finanças Públicas e Orçamento": "Economia",
    "Esporte e Lazer, Finanças Públicas e Orçamento": "Economia",
    "Turismo": "Economia",
    "Comunicações": "Economia",
    "Direito e Defesa do Consumidor, Energia, Recursos Hídricos e Minerais, Finanças Públicas e Orçamento": "Economia",
    "Economia, Finanças Públicas e Orçamento, Relações Internacionais e Comércio Exterior": "Economia",
    "Economia, Finanças Públicas e Orçamento, Indústria, Comércio e Serviços, Relações Internacionais e Comércio Exterior": "Economia",
    "Economia, Indústria, Comércio e Serviços": "Economia",
    "Finanças Públicas e Orçamento, Indústria, Comércio e Serviços": "Economia",
    "Administração Pública, Economia, Finanças Públicas e Orçamento": "Economia",
    "Administração Pública, Finanças Públicas e Orçamento": "Economia",
    "Administração Pública, Ciência, Tecnologia e Inovação": "Economia",
    "Administração Pública, Ciência, Tecnologia e Inovação, Viação, Transporte e Mobilidade": "Economia",
    "Administração Pública, Comunicações": "Economia",
    "Administração Pública, Indústria, Comércio e Serviços, Turismo": "Economia",
    "Administração Pública, Relações Internacionais e Comércio Exterior": "Economia",
    "Arte, Cultura e Religião, Economia, Homenagens e Datas Comemorativas, Turismo": "Economia",
    "Agricultura, Pecuária, Pesca e Extrativismo, Finanças Públicas e Orçamento": "Economia",

    "Homenagens e Datas Comemorativas, Viação, Transporte e Mobilidade": "Homenagens",
    "Esporte e Lazer, Homenagens e Datas Comemorativas": "Homenagens",
    "Arte, Cultura e Religião, Homenagens e Datas Comemorativas": "Homenagens",
    "Administração Pública, Homenagens e Datas Comemorativas": "Homenagens",
    "Comunicações, Homenagens e Datas Comemorativas": "Homenagens"

}

def mapear_categoria_tema(temas):
    if pd.isna(temas):
        return "Indefinido"
    temas = temas.lower()
    for chave, categoria in mapa_temas.items():
        if chave in temas:
            return categoria
    for chave, categoria in mapa_temas_completo.items():
        if chave.lower() == temas:
            return categoria
    return "Outro"

def distribuicao_aprovados(df):
    # Gerar gráfico de distribuição de aprovados
    distribuicao_aprovados = df['aprovado'].value_counts()
    distribuicao_aprovados.index = distribuicao_aprovados.index.map({0: 'Reprovado', 1: 'Aprovado'})

    plt.figure(figsize=(6, 4))
    distribuicao_aprovados.plot(kind='bar', color=['red', 'green'])
    #plt.title('Distribuição de Projetos Aprovados')
    #plt.xlabel('Aprovado')
    plt.ylabel('Projetos de Lei', fontsize=20)
    plt.xticks(rotation=0, fontsize=20)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.show()

def distribuicao_temas(df):
    # Gerar gráfico de distribuição de aprovados
    distribuicao_temas = df['tema_dominante2'].value_counts()
    plt.figure(figsize=(6, 4))
    distribuicao_temas.plot(kind='bar', color=['red', 'green', 'blue', 'orange', 'purple', 'yellow'])
    plt.title('Distribuição de Projetos por Temas Dominantes')
    plt.xlabel('Temas')
    plt.ylabel('Quantidade de Projetos')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def distribuicao_regiao(df):
    # Gerar gráfico de distribuição de aprovados
    distribuicao_regiao = df['região'].value_counts()
    plt.figure(figsize=(6, 4))
    distribuicao_regiao.plot(kind='bar', color=['red', 'green', 'blue', 'orange', 'purple', 'yellow'])
    plt.title('Distribuição de Projetos por Região')
    plt.xlabel('Região')
    plt.ylabel('Quantidade de Projetos')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def distribuicao_bloco(df):
    # Gerar gráfico de distribuição de aprovados
    distribuicao_bloco = df['bloco_partidario'].value_counts()
    plt.figure(figsize=(6, 4))
    distribuicao_bloco.plot(kind='bar', color=['red', 'green', 'blue', 'orange', 'purple', 'yellow'])
    plt.title('Distribuição de Projetos por Bloco Partidário')
    plt.xlabel('Bloco Partidário')
    plt.ylabel('Quantidade de Projetos')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def balancear_aprovados(df):
    # Garantir que a coluna 'aprovado' seja binária (0 e 1)
    #df['aprovado'] = df['aprovado'].astype(int)

    # Selecione colunas numéricas/categóricas para balancear
    # Aqui, como exemplo, vamos usar todas menos a target
    X = df.drop(columns=['aprovado'])
    y = df['aprovado']

    encoders = {}
    # Converter variáveis categóricas com LabelEncoder
    for col in X.select_dtypes(include='object').columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le  # guardar para decodificação

    # Aplicar SMOTE
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)

    X_res_decodificado = X_res.copy()
    for col, le in encoders.items():
        X_res_decodificado[col] = le.inverse_transform(X_res[col])

    # Criar DataFrame final balanceado com colunas originais restauradas
    df_balanceado = X_res_decodificado.copy()
    df_balanceado['aprovado'] = y_res
    return df_balanceado

df = pd.read_excel("../projetos_PL_2021_2024_transformado.xlsx")
#Converte em finalizado todos os aprovados
df.loc[df['aprovado'] == True, 'finalizado'] = True
# Remover linhas onde 'finalizado' é False
df = df[df['finalizado'] == True]
df = df[df['uf_principal'] != "?"]
df["tema_dominante2"] = df["temas"].apply(mapear_categoria_tema)

#### Ante do balanceamento
print(len(df)) #580
colunas = ['ano', 'região', 'dias_tramitacao', 'tema_dominante2', 'bloco_partidario', 'autoria_coletiva', 'aprovado']
df = df[colunas]
X = df.drop(columns=["aprovado"])
y = df["aprovado"].astype(int)
#separar treino de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
df_treino = X_train
df_treino["aprovado"] = y_train
print(len(df_treino)) #580
distribuicao_aprovados(df_treino)
#distribuicao_bloco(df)
#distribuicao_regiao(df)
#distribuicao_temas(df)
df_balanceado = balancear_aprovados(df_treino)
df_balanceado.to_excel("final.xlsx", index=False)
### Depois do Balanceamento
print(len(df_balanceado)) # 982
distribuicao_aprovados(df_balanceado)
df_teste = X_test
df_teste["aprovado"] = y_test
df_teste.to_excel("df_teste.xlsx", index=False)
