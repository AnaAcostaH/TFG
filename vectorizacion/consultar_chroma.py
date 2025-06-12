import chromadb
import re
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Inicializa cliente y modelo
chroma_client = chromadb.PersistentClient(path="./vectorizacion/db")
collection = chroma_client.get_or_create_collection(name="productos")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def consultar_producto(pregunta, k=10):
    # Convierte la pregunta a embedding
    pregunta_embedding = embedding_model.encode(pregunta).tolist()

    # Busca los k productos más similares
    resultados = collection.query(
        query_embeddings=[pregunta_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    productos = []
    for doc, meta in zip(resultados["documents"][0], resultados["metadatas"][0]):
        productos.append({
            "nombre": doc,
            "precio": meta["precio"],
            "supermercado": meta["supermercado"],
            "seccion": meta.get("seccion", ""),
            "url": meta["url"]
        })

    # Limpieza y conversión
    productos_limpios = []
    for p in productos:
        try:
            # Elimina caracteres como €, espacios no estándar, etc.
            precio_str = re.sub(r"[^\d,\.]", "", str(p["precio"]))
            precio_str = precio_str.replace(",", ".")
            precio_float = float(precio_str)

            p["precio"] = precio_float
            productos_limpios.append(p)
        except Exception as e:
            continue  # ignora productos no parseables

    # Ordenar por precio
    productos_ordenados = sorted(productos_limpios, key=lambda x: x["precio"])
    for prod in productos_ordenados:
        print(f"- {prod['nombre']} | {prod['precio']}€ en {prod['supermercado']}")
    return productos_ordenados

def comparar_lista_de_la_compra(productos_input: str, k_por_producto: int = 30):
    productos_lista = [p.strip() for p in productos_input.split(",") if p.strip()]
    supermercados = ["mercadona", "alcampo", "ahorramas"]
    
    urls_supermercados = {
        "mercadona": "https://www.mercadona.es",
        "alcampo": "https://www.alcampo.es",
        "ahorramas": "https://www.ahorramas.com"
    }

    totales = {}
    detalles_supermercado = {}

    for supermercado in supermercados:
        total = 0.0
        detalles = []

        for producto in productos_lista:
            resultados = consultar_producto(producto, k=k_por_producto)
            resultados_super = [
                r for r in resultados if r["supermercado"].lower() == supermercado
            ]

            if resultados_super:
                mejor = min(resultados_super, key=lambda r: r["precio"])
                detalles.append((producto, mejor["nombre"], mejor["precio"]))
                total += mejor["precio"]
            else:
                detalles.append((producto, None, None))

        if any(p[2] is not None for p in detalles):
            totales[supermercado] = total
        else:
            totales[supermercado] = float("inf")

        detalles_supermercado[supermercado] = detalles

    # Ordenar supermercados por total
    supermercados_ordenados = sorted(
        supermercados, key=lambda s: totales[s]
    )

    print("\n🛒 Resultado de la búsqueda:")
    for supermercado in supermercados_ordenados:
        detalles = detalles_supermercado[supermercado]
        total = totales[supermercado]
        encontrados = sum(1 for _, _, precio in detalles if precio is not None)
        if total == float("inf"):
            continue

        print(f"\n✅ {supermercado.capitalize()} → {round(total, 2)}€ ({encontrados}/{len(productos_lista)} productos encontrados)")
        for entrada_usuario, nombre_encontrado, precio in detalles:
            if nombre_encontrado:
                print(f"   - {entrada_usuario} → {nombre_encontrado} ({precio}€)")
            else:
                print(f"   - {entrada_usuario} → ❌ No encontrado")

    # Mostrar solo el supermercado más barato
    disponibles = [(s, t) for s, t in totales.items() if t != float("inf")]
    if disponibles:
        supermercado_mas_barato, precio_total = min(disponibles, key=lambda x: x[1])
        print("Supermercado más barato para tu lista:")
        url = urls_supermercados.get(supermercado_mas_barato.lower(), "#")
        print(f"👉 [{supermercado_mas_barato.capitalize()} → {round(precio_total, 2)}€]({url})")
    else:
        print("Ningún supermercado tiene los productos de tu lista.")

    return [(s, totales[s], detalles_supermercado[s]) for s in supermercados if totales[s] != float("inf")]
