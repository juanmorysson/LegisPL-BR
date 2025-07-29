import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier

# Carregar o dataset
df = pd.read_excel("final.xlsx")

# Preparar dados
X_train = df.drop(columns=["aprovado"])
y_train = df["aprovado"].astype(int)

# Carregar o dataset_test
df = pd.read_excel("df_teste.xlsx")

# Preparar dados
X_test = df.drop(columns=["aprovado"])
y_test = df["aprovado"].astype(int)

# Codificar colunas categóricas
colunas_categoricas = X_train.select_dtypes(include='object').columns
encoders = {}
for col in colunas_categoricas:
    le = LabelEncoder()
    X_train[col] = le.fit_transform(X_train[col].astype(str))
    encoders[col] = le

for col in colunas_categoricas:
    le = encoders[col][0]
    X_test[col] = le.fit_transform(X_test[col].astype(str))

def regressao_logistica():
    # GridSearch para Logistic Regression
    param_grid = {
        "C": [0.01, 0.1, 1],
        "penalty": ["l2"],
        "solver": ["lbfgs", "liblinear", "saga"]
    }
    modelo = LogisticRegression(max_iter=20000)
    grid = GridSearchCV(modelo, param_grid, cv=3, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Avaliação
    y_pred = grid.predict(X_test)
    print("Melhores hiperparâmetros:", grid.best_params_)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Matriz de confusão
    disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=["Não", "Sim"])
    disp.plot(cmap='Blues', text_kw={'fontsize': 22})
    plt.title("Regressão Logística", fontsize=22)
    plt.xlabel("Predito", fontsize=22)
    plt.ylabel("Real", fontsize=22)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig("cm - regressão logística.png")
    #plt.show()


def rf():
    # Definir grid de hiperparâmetros
    param_grid_rf = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20]
    }

    # Treinar modelo com GridSearch
    modelo_rf = RandomForestClassifier(random_state=42)
    grid = GridSearchCV(modelo_rf, param_grid_rf, cv=3, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Previsões e avaliação
    y_pred = grid.predict(X_test)
    print("Melhores hiperparâmetros:", grid.best_params_)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Matriz de confusão
    disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=["Não", "Sim"])
    disp.plot(cmap='Blues', text_kw={'fontsize': 22})
    plt.title("Random Forest", fontsize=22)
    plt.xlabel("Predito", fontsize=22)
    plt.ylabel("Real", fontsize=22)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig("cm - rf.png")
    #plt.show()

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

    # Matriz de confusão
    disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=["Não", "Sim"])
    disp.plot(cmap='Blues', text_kw={'fontsize': 22})
    plt.title("XGBoost", fontsize=22)
    plt.xlabel("Predito", fontsize=22)
    plt.ylabel("Real", fontsize=22)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig("cm - XGBoost.png")
    #plt.show()

def mlp():
    # Escalar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, stratify=y, test_size=0.25, random_state=42)

    # Grid de hiperparâmetros
    param_grid_mlp = {
        'hidden_layer_sizes': [(50,), (100,), (50, 50)],
        'activation': ['relu', 'tanh', 'logistic']
    }

    # Modelo e grid
    modelo_mlp = MLPClassifier(max_iter=10000, random_state=42)
    grid = GridSearchCV(modelo_mlp, param_grid_mlp, cv=3, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Avaliação
    y_pred = grid.predict(X_test)
    print("Melhores hiperparâmetros:", grid.best_params_)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Matriz de confusão
    disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=["Não", "Sim"])
    disp.plot(cmap='Blues', text_kw={'fontsize': 22})
    plt.title("MLP", fontsize=22)
    plt.xlabel("Predito", fontsize=22)
    plt.ylabel("Real", fontsize=22)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.savefig("cm - mlp.png")
    #plt.show()
regressao_logistica()
rf()
xgb()
mlp()

'''
Rregressão Logística
Melhores hiperparâmetros: {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}

Classification Report:
               precision    recall  f1-score   support

           0       0.64      0.65      0.65       123
           1       0.64      0.63      0.64       123

    accuracy                           0.64       246
   macro avg       0.64      0.64      0.64       246
weighted avg       0.64      0.64      0.64       246

Random Forest
Melhores hiperparâmetros: {'max_depth': None, 'n_estimators': 200}

Classification Report:
               precision    recall  f1-score   support

           0       0.92      0.84      0.88       123
           1       0.85      0.93      0.89       123

    accuracy                           0.88       246
   macro avg       0.89      0.88      0.88       246
weighted avg       0.89      0.88      0.88       246

XGBoost
Melhores hiperparâmetros: {'learning_rate': 0.3, 'max_depth': 7, 'n_estimators': 300}

Classification Report:
               precision    recall  f1-score   support

           0       0.92      0.85      0.89       123
           1       0.86      0.93      0.89       123

    accuracy                           0.89       246
   macro avg       0.89      0.89      0.89       246
weighted avg       0.89      0.89      0.89       246

MLP
Melhores hiperparâmetros: {'activation': 'relu', 'hidden_layer_sizes': (50, 50)}

Classification Report:
               precision    recall  f1-score   support

           0       0.80      0.76      0.78       123
           1       0.77      0.81      0.79       123

    accuracy                           0.78       246
   macro avg       0.79      0.78      0.78       246
weighted avg       0.79      0.78      0.78       246
'''