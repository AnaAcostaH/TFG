# 🛒 Comparador de precios entre supermercados

Este proyecto permite comparar los precios de productos en **Mercadona**, **Alcampo** y **Ahorramás** mediante procesamiento semántico con embeddings y una interfaz de usuario.

Usa `sentence-transformers` para buscar coincidencias semánticas entre lo que escribe el usuario y los productos indexados desde los CSV. Además, ofrece una interfaz con **Gradio** para hacerlo de forma visual.

---

## 🚀 Funcionalidades

* 🔎 Comparación automática de productos por supermercado.
* 🧠 Búsqueda semántica con embeddings (MiniLM).
* 💾 Datos indexados con **ChromaDB**.
* 🖥️ Interfaz visual con Gradio.
* 🧾 Soporte para consultas simples o listas de la compra.

---

## 🧱 Estructura del proyecto

```bash
TFG/
│
├── constants/
│ └── constants.py # (Opcional) Configuraciones generales
│
├── consultas/
│ └── preguntar_producto.py # Consola interactiva de búsqueda
│
├── data/
│ ├── alcampo_productos.csv
│ ├── ahorramas_productos.csv
│ └── mercadona_productos.csv # Datos brutos por supermercado
│
├── interfaz/
│ └── gradio_app.py # Interfaz visual web con Gradio
│
├── limpieza/
│ └── normalizacion.py # Limpieza y normalización de textos
│
├── scraping/
│ └── web-scraping.py # Código de scraping para obtener productos
│
├── vectorizacion/
│ ├── cargar_chroma_db.py # Carga de embeddings y vectorización en Chroma
│ └── consultar_chroma.py # Consultas a la base vectorial
│
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo
```

---

## ▶️ Uso

### 1. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 2. Vectorización de productos (una sola vez)

```bash
python vectorizacion/cargar_chroma_db.py
```

### 3. Ejecutar la interfaz web

```bash
python interfaz/gradio_app.py
```

### 4. O usar la consola

```bash
python consultas/preguntar_producto.py
```

---

## 🧠 Embeddings
Se utiliza el modelo all-MiniLM-L6-v2 de sentence-transformers para vectorizar los productos y realizar búsquedas semánticas.

## 💡 Ejemplo visual (terminal)

```
¿Qué buscas? > leche entera, huevos camperos, jamon serrano

✅ Mercadona → 3.06€ (3/3 productos encontrados)
   - leche entera → leche entera hacendado (0.97€)
   - huevos camperos → picos camperos de jerez hacendado (0.99€)
   - jamon serrano → pate de jamon hacendado (1.1€)

✅ Ahorramás → 3.81€
✅ Alcampo → 7.44€

---

🏆 Supermercado más barato:
👉 [Mercadona](https://www.mercadona.es) → 3.06€
```

---

## 🌐 Supermercados compatibles

* 🟢 [Mercadona](https://www.mercadona.es)
* 🔵 [Alcampo](https://www.alcampo.es)
* 🟡 [Ahorramás](https://www.ahorramas.com)

---

## 📦 Requisitos (requirements.txt)

```txt
chromadb
sentence-transformers
gradio
pandas
```

---

## 🛠 Recomendaciones

* Ejecuta la vectorización solo si añades nuevos productos o cambias los CSV.
* Puedes adaptar el sistema para otros supermercados cambiando los CSV y actualizando la vectorización.

---

## 📸 Captura web Gradio

> Puedes ver la interfaz en tu navegador tras ejecutar `gradio_app.py`. Se ve algo así:

![image](https://github.com/user-attachments/assets/3fe2c79a-a9a6-4b4a-9dd6-b0b092e9807e)


---

