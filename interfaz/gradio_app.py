import sys
import os
import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import tempfile
from datetime import datetime
import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from vectorizacion.consultar_chroma import comparar_lista_de_la_compra
from utils.consultar_historico import obtener_historico
from utils.consultar_historico import obtener_grafico_minimos

def comparar_interface(productos_input):
    resultados = comparar_lista_de_la_compra(productos_input, k_por_producto=30)
    
    if not resultados:
        return "⚠️ No se encontraron coincidencias para tu lista."

    mensaje = "## 🛒 Resultado de la búsqueda:\n"
    datos_export = {}
    
    for supermercado, total, detalles in sorted(resultados, key=lambda x: x[1]):
        mensaje += f"\n### 🧾 {supermercado.capitalize()} → **{round(total, 2)}€**"
        mensaje += f"\n_{sum(1 for _, _, p in detalles if p is not None)}/{len(detalles)} productos encontrados_\n"
        productos = []
        for entrada_usuario, nombre_encontrado, precio in detalles:
            if nombre_encontrado:
                mensaje += f"- **{entrada_usuario}** → {nombre_encontrado} (**{precio}€**)\n"
                productos.append({"input": entrada_usuario, "producto": nombre_encontrado, "precio": precio})
            else:
                mensaje += f"- **{entrada_usuario}** →  No encontrado\n"
                productos.append({"input": entrada_usuario, "producto": None, "precio": None})
                
        datos_export[supermercado] = {
            "total": round(total, 2),
            "productos": productos
        }

    supermercado_mas_barato, total_mas_barato, _ = min(resultados, key=lambda x: x[1])
    url = {
        "mercadona": "https://www.mercadona.es",
        "alcampo": "https://www.alcampo.es",
        "ahorramas": "https://www.ahorramas.com"
    }.get(supermercado_mas_barato.lower(), "#")

    #mensaje += f"\n---\n\n🏆 **Supermercado más barato:** [{supermercado_mas_barato.capitalize()} → {round(total_mas_barato, 2)}€]({url})"
    mensaje += (
        "\n---\n\n"
        f"<h2 style='text-align: center;'>📉 Supermercado más barato</h2>"
        f"<h3 style='text-align: center;'><a href='{url}' target='_blank'>{supermercado_mas_barato.capitalize()}</a> → {round(total_mas_barato, 2)}€</h3>"
    )

    # Crear archivos temporales
    temp_dir = tempfile.gettempdir()

    json_path = os.path.join(temp_dir, "resultado.json")
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(datos_export, f_json, indent=4, ensure_ascii=False)

    pdf_path = os.path.join(temp_dir, "resultado.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Fuente DejaVu con estilos
    ruta_fuente = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", ruta_fuente)
    pdf.add_font("DejaVu", "B", ruta_fuente)
    pdf.set_font("DejaVu", "B", 16)

    # Título principal
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 12, text="Resultado de tu búsqueda de la compra", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, text=f"Fecha: {fecha_actual}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # Supermercados y productos
    for supermercado, info in datos_export.items():
        pdf.set_font("DejaVu", "B", 13)
        pdf.cell(0, 10, text=f"{supermercado.capitalize()} - Total: {info['total']} €", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("DejaVu", "", 12)
        for p in info["productos"]:
            linea = f"• {p['input']} → {p['producto']} ({p['precio']} €)" if p['producto'] else f"• {p['input']} → No encontrado"
            pdf.cell(0, 8, text=linea, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

    pdf.output(pdf_path)

    return mensaje, json_path, pdf_path

# Interfaz visual 
with gr.Blocks() as demo:
    gr.Markdown("# 🛍️ Comparador de precios de supermercados")
    gr.Markdown("Escribe una lista de productos separados por comas. Ej: `leche entera, huevos camperos, jamon serrano`")
    
    with gr.Row():
        entrada = gr.Textbox(
            lines=2,
            placeholder="Ej: leche entera, huevos camperos, jamon serrano",
            label="Productos"
        )

    boton = gr.Button("🔍 Comparar precios")
    salida = gr.Markdown()

    with gr.Row():
        descarga_json = gr.File(label="Descargar JSON", visible=False)
        descarga_pdf = gr.File(label="Descargar PDF", visible=False)

    def comparar_y_mostrar(productos_input):
        mensaje, json_path, pdf_path = comparar_interface(productos_input)
        return mensaje, gr.update(value=json_path, visible=True), gr.update(value=pdf_path, visible=True)

    boton.click(fn=comparar_y_mostrar, inputs=entrada, outputs=[salida, descarga_json, descarga_pdf])

    with gr.Accordion("📊 Consultar histórico de precios", open=False):
        producto_historico = gr.Textbox(label="Nombre del producto", placeholder="Ej: leche entera")
        boton_historico = gr.Button("🔎 Ver histórico")
        salida_grafico = gr.Plot(label="Evolución del precio")

        def consultar_y_mostrar(producto_nombre):
            fig = obtener_grafico_minimos(producto_nombre)
            return fig  


        boton_historico.click(
            fn=consultar_y_mostrar,
            inputs=producto_historico,
            outputs=[salida_grafico]
        )

demo.launch()
