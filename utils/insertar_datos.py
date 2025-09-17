# utils/insertar_datos.py
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "historico_precios.db")

def insertar_datos_en_db(productos):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    for p in productos:
        try:
            cursor.execute(
                "INSERT INTO historico_precios (supermercado, producto, precio, fecha) VALUES (?, ?, ?, ?)",
                (p["supermercado"], p["nombre_limpio"], p["precio"], fecha_actual)
            )
        except Exception as e:
            print(f"❌ Error insertando '{p['nombre_limpio']}': {e}")

    conn.commit()
    conn.close()
    print("✅ Inserción en base de datos finalizada.")
