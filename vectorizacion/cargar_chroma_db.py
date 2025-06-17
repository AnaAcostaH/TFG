import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Inicializa cliente local de ChromaDB
chroma_client = chromadb.PersistentClient(path="./vectorizacion/db")

# Carga modelo de embeddings (en mi caso all-MiniLM-L6-v2)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Crea o accede a la colección de productos
collection = chroma_client.get_or_create_collection(name="productos")

# Ruta a los CSVs de los supermercados
carpeta_csv = "./data"

def batch(iterable, batch_size=5000):
    # Divide una lista en lotes
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

# Cargar todos los archivos CSV de la carpeta
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith(".csv"):
        df = pd.read_csv(os.path.join(carpeta_csv, archivo))

        # Filtrar filas con valores nulos
        df = df.dropna(subset=["nombre_limpio", "precio"])

        # Genera embeddings del nombre del producto
        textos = df["nombre_limpio"].tolist()
        embeddings = embedding_model.encode(textos).tolist()

        # Asocia metadatos a esos embeddings y crea un id por cada producto
        metadatas = df[["supermercado", "precio", "seccion", "url"]].to_dict(orient="records")
        ids = [f"{archivo}_{i}" for i in range(len(df))]

        # Carga datos por lotes para que vaya más rápido
        for t_batch, e_batch, m_batch, id_batch in zip(
            batch(textos), batch(embeddings), batch(metadatas), batch(ids)
        ):
            collection.add(
                documents=t_batch,
                embeddings=e_batch,
                metadatas=m_batch,
                ids=id_batch
            )

print("Productos cargados en ChromaDB.")
