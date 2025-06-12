import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from vectorizacion.consultar_chroma import consultar_producto, comparar_lista_de_la_compra

# Inicializar cliente y modelo
chroma_client = chromadb.PersistentClient(path="./vectorizacion/db")
collection = chroma_client.get_or_create_collection("productos")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("🛒 Bienvenido al comparador de precios. \nEscribe un producto o una lista separada por comas (ej: leche, huevos, galletas).")
print("Escribe 'salir' para terminar.\n")

while True:
    pregunta = input("¿Qué buscas? > ").strip()
    if pregunta.lower() in ["salir", "exit", "quit"]:
        print("👋 ¡Hasta pronto!")
        break

    if "," in pregunta:
        resultados = comparar_lista_de_la_compra(pregunta, k_por_producto=30)

        # Mostrar advertencia si no se encontró nada en ningún supermercado
        encontrados = any(
            any(p[2] is not None for p in detalles)
            for _, _, detalles in resultados
        )
        if not encontrados:
            print("No se encontraron coincidencias para tu lista.")
