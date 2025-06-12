import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from vectorizacion.consultar_chroma import comparar_lista_de_la_compra

def comparar_interface(productos_input):
    resultados = comparar_lista_de_la_compra(productos_input, k_por_producto=30)
    
    if not resultados:
        return "⚠️ No se encontraron coincidencias para tu lista."

    mensaje = "## 🛒 Resultado de la búsqueda:\n"
    for supermercado, total, detalles in sorted(resultados, key=lambda x: x[1]):
        mensaje += f"\n### 🧾 {supermercado.capitalize()} → **{round(total, 2)}€**"
        mensaje += f"\n_{sum(1 for _, _, p in detalles if p is not None)}/{len(detalles)} productos encontrados_\n"
        for entrada_usuario, nombre_encontrado, precio in detalles:
            if nombre_encontrado:
                mensaje += f"- **{entrada_usuario}** → {nombre_encontrado} (**{precio}€**)\n"
            else:
                mensaje += f"- **{entrada_usuario}** →  No encontrado\n"

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

    return mensaje

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

    boton.click(fn=comparar_interface, inputs=entrada, outputs=salida)

demo.launch()
