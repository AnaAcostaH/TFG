import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import supermercados_config

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

# Función para hacer scroll dinámico y cargar los productos
def cargar_todos_los_productos(driver, selector_producto, scroll_pause_time=3, max_scrolls=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        try:
            WebDriverWait(driver, scroll_pause_time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_producto))
            )
        except Exception as e:
            print(f"Timeout al cargar productos: {e}")
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1
    print(f"Scrolls realizados: {scrolls}")

def cargar_todos_los_productos_ahorramas(driver, boton_selector, producto_selector, max_clicks=50, wait_time=3):
    clicks = 0
    while clicks < max_clicks:
        try:
            boton = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, boton_selector))
            )
            boton.click()
            time.sleep(wait_time)
            clicks += 1
            print(f"🔄 Clic en 'Más resultados' ({clicks}/{max_clicks})")
        except:
            print("✅ No hay más productos para cargar.")
            break
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, producto_selector))
    )

def scrape_supermercado(supermercado, url, selectores, driver):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selectores["producto"]))
        )
        if supermercado == "alcampo":
            print("Realizando scroll para cargar productos...")
            cargar_todos_los_productos(driver, selectores["producto"])
        if supermercado == "ahorramas":
            print("Cargando todos los productos en Ahorramas...")
            cargar_todos_los_productos_ahorramas(driver, selectores["boton_mas_resultados"], selectores["producto"])  
        productos = []
        index = 0
        while True:
            items = driver.find_elements(By.CSS_SELECTOR, selectores["producto"])
            if index >= len(items):
                break
            try:
                item = items[index]
                driver.execute_script("arguments[0].scrollIntoView();", item)
                time.sleep(0.5)
                items = driver.find_elements(By.CSS_SELECTOR, selectores["producto"])
                item = items[index]
                nombre_element = item.find_element(By.CSS_SELECTOR, selectores["nombre"])
                precio_element = item.find_element(By.CSS_SELECTOR, selectores["precio"])
                nombre = nombre_element.text.strip() if nombre_element else ""
                precio = precio_element.text.strip() if precio_element else ""
                if not nombre:
                    nombre = nombre_element.get_attribute("innerHTML").strip()
                if not precio:
                    precio = precio_element.get_attribute("innerHTML").strip()
                if nombre and precio:
                    productos.append({"supermercado": supermercado, "nombre": nombre, "precio": precio, "url": url})
                    print(f"✅ Producto {index + 1}: {nombre} - {precio}")
                index += 1
            except Exception as e:
                print(f" Error procesando producto {index + 1}: {e}")
                index += 1
    except Exception as e:
        print(f" Error al procesar la página de {supermercado}: {e}")
    return productos

def main():
    driver = webdriver.Chrome(options=options)
    try:
        for supermercado, config in supermercados_config.items():
            all_data = []
            for seccion, url in config["secciones"].items():
                data = scrape_supermercado(supermercado, url, config["selectores"], driver)
                for item in data:
                    item["seccion"] = seccion
                all_data.extend(data)
            if all_data:
                df = pd.DataFrame(all_data)
                super = "C:/Users/Usuario/Documentos/TFG/" + supermercado + "_productos.csv"
                df.to_csv(super, index=False)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
