import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "historico_precios.db")

def obtener_historico(producto_nombre):
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT producto, supermercado, precio, fecha
        FROM historico_precios
        WHERE producto LIKE ?
        ORDER BY fecha;
    """
    df = pd.read_sql_query(query, conn, params=(f"%{producto_nombre}%",))
    conn.close()
    return df

def obtener_grafico_minimos(producto_nombre):
    df = obtener_historico(producto_nombre)

    if df.empty:
        fig, ax = plt.subplots()
        ax.set_title("No hay datos disponibles")
        return fig

    # Convertir fecha a datetime
    df["fecha"] = pd.to_datetime(df["fecha"])


    # Seleccionar fechas disponibles
    fechas_disponibles = sorted(df["fecha"].unique())
    if len(fechas_disponibles) >= 4:
        ultimas_fechas = fechas_disponibles[-4:]
    else:
        ultimas_fechas = fechas_disponibles  # usar todas las fechas disponibles

    df_filtrado = df[df["fecha"].isin(ultimas_fechas)]

    # Obtener mínimo por supermercado y fecha
    df_minimos = (
        df_filtrado.groupby(["fecha", "supermercado"])["precio"]
        .min()
        .reset_index()
    )

    # Graficar
    fig, ax = plt.subplots()
    for supermercado in df_minimos["supermercado"].unique():
        datos_super = df_minimos[df_minimos["supermercado"] == supermercado]
        ax.plot(datos_super["fecha"], datos_super["precio"], marker='o', label=supermercado)

    ax.set_title(f"Evolución de precios mínimos para '{producto_nombre}'")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio mínimo (€)")
    ax.legend()
    fig.autofmt_xdate(rotation=45)

    return fig
