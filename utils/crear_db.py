import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "historico_precios.db")

def crear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supermercado TEXT NOT NULL,
            producto TEXT NOT NULL,
            precio REAL,
            fecha TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print(f"Base de datos y tabla creadas en {DB_PATH}")

if __name__ == "__main__":
    crear_db()
