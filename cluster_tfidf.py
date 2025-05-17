import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import umap.umap_ as umap

nltk.download('stopwords')
stopwords_pt = stopwords.words('portuguese')

# Carregar ementas
df = pd.read_excel("projetos_PL_2024_transformado.xlsx")  # ou outro nome de arquivo
ementas = df['ementa'].fillna("")

# Vetorização TF-IDF
vectorizer = TfidfVectorizer(max_df=0.8, min_df=3, stop_words=stopwords_pt)
X = vectorizer.fit_transform(ementas)

# Escolher número de clusters (K)
k = 5
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster_kmeans"] = kmeans.fit_predict(X)

# Mostrar exemplos
for i in range(k):
    print(f"\n--- Cluster {i} ---")
    print(df[df["cluster_kmeans"] == i]["ementa"].head(3).to_string(index=False))

# Redução de dimensionalidade com UMAP
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(X.toarray())

df["x_umap"] = X_umap[:, 0]
df["y_umap"] = X_umap[:, 1]

# Plot
plt.figure(figsize=(10, 6))
for i in range(k):
    plt.scatter(
        df[df["cluster_kmeans"] == i]["x_umap"],
        df[df["cluster_kmeans"] == i]["y_umap"],
        label=f"Cluster {i}",
        alpha=0.6
    )
plt.legend()
plt.title("Clusters de Ementas de Projetos de Lei (TF-IDF + UMAP)")
plt.xlabel("UMAP X")
plt.ylabel("UMAP Y")
plt.grid(True)
plt.tight_layout()
plt.savefig("umaptdidf.png")
plt.show()

# Salvar no Excel
df.to_excel("projetos_PL_clusters_umap.xlsx", index=False)
print("Arquivo salvo como 'projetos_PL_clusters_umap.xlsx'")