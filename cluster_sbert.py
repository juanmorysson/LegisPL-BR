import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import umap.umap_ as umap

# Carregar dados
df = pd.read_excel("projetos_PL_2024_transformado.xlsx")
ementas = df['ementa'].fillna("").tolist()

# SBERT: transformer para sentenças em português
modelo = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
embeddings = modelo.encode(ementas, show_progress_bar=True)

# Clustering com KMeans
k = 5
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster_sbert'] = kmeans.fit_predict(embeddings)

# Mostrar exemplos por cluster
for i in range(k):
    print(f"\n--- Cluster {i} ---")
    print(df[df["cluster_sbert"] == i]["ementa"].head(3).to_string(index=False))

# Redução de dimensionalidade com UMAP
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(embeddings)

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
plt.title("Clusters de Ementas de Projetos de Lei (SBERT + UMAP)")
plt.xlabel("UMAP X")
plt.ylabel("UMAP Y")
plt.grid(True)
plt.tight_layout()
plt.savefig("umapSBERT.png")
plt.show()

# Salvar no Excel
df.to_excel("projetos_PL_clusters_umap.xlsx", index=False)
print("Arquivo salvo como 'projetos_PL_clusters_umap_SBERT.xlsx'")