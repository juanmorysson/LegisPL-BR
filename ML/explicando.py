import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
import shap

# Carregar o dataset
df = pd.read_excel("final2.xlsx")
# Preparar dados
X = df.drop(columns=["aprovado"])
y = df["aprovado"].astype(int)

# Codificar colunas categóricas
colunas_categoricas = X.select_dtypes(include='object').columns
encoders = {}
for col in colunas_categoricas:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

# Ver o mapeamento da coluna 'temas_dominantes'
encoder_tema = encoders['tema_dominante']

# Mostrar os pares (número → categoria)
for i, classe in enumerate(encoder_tema.classes_):
    print(f"{i}: {classe}")

# Ver o mapeamento da coluna 'temas_dominantes'
encoder_regiao = encoders['região']

# Mostrar os pares (número → categoria)
for i, classe in enumerate(encoder_regiao.classes_):
    print(f"{i}: {classe}")

# Ver o mapeamento da coluna 'temas_dominantes'
encoder_bloco = encoders['bloco_partidario']

# Mostrar os pares (número → categoria)
for i, classe in enumerate(encoder_bloco.classes_):
    print(f"{i}: {classe}")



X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

def xgb():
    # Definir grid de hiperparâmetros
    param_grid_xgb = {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.1, 0.3]
    }

    # Treinar modelo com GridSearch
    modelo_xgb = XGBClassifier(eval_metric='logloss', random_state=42)
    grid = GridSearchCV(modelo_xgb, param_grid_xgb, cv=3, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Avaliar
    y_pred = grid.predict(X_test)
    print("Melhores hiperparâmetros:", grid.best_params_)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Obter o melhor modelo treinado
    best_model = grid.best_estimator_

    # Criar o objeto explainer para o modelo XGBoost
    explainer = shap.Explainer(best_model, X_train.astype(float))

    print(type(explainer))
    # Calcular os valores SHAP para o conjunto de teste
    shap_values = explainer(X_test.astype(float))

    # Gerar o gráfico beeswarm
    shap.plots.beeswarm(shap_values, max_display=10)

    # Exibir o gráfico
    plt.tight_layout()
    plt.show()



xgb()

