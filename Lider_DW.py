
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import ftfy
import datetime

def run():
    def obtener_texto(elemento, clase):
        try:
            texto = elemento.find_element(By.CLASS_NAME, clase).text
            return ftfy.fix_text(texto)
        except NoSuchElementException:
            return ""
        
    def obtener_texto2(elemento, xpath):
        try:
            texto = elemento.find_element(By.XPATH, xpath).text
            return ftfy.fix_text(texto)
        except NoSuchElementException:
            return ""

    def obtener_atributo(elemento, xpath, atributo):
        try:
            return elemento.find_element(By.XPATH, xpath).get_attribute(atributo)
        except NoSuchElementException:
            return ""  

    # Inicia el WebDriver
    driver_service = Service(executable_path="C:\\Users\\man27\\Desktop\\AI_test\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    # Navega a la página web
    website = 'https://www.lider.cl/supermercado/category/Limpieza_y_Aseo/Ba%C3%B1o_y_Cocina/Lavaloza_y_Lavavajilla?page=1&hitsPerPage=16'  # Asegúrate de que esta URL sea la correcta
    driver.get(website)
    time.sleep(10)


    pagina_actual = 1# Asume que la primera página es 1
    max_paginas = 4 #usta este valor al número máximo de páginas que deseas procesar

    fecha_actual = datetime.datetime.now()
    semana_actual = fecha_actual.strftime("%U")
    dia_actual = fecha_actual.strftime("%d-%m-%Y")
    #hora_actual = datetime.datetime.now().strftime('%H:%M:%S')

    supermercado ="Lider"

    info=[]
    while pagina_actual <= max_paginas:
        productos = driver.find_elements(By.CLASS_NAME,"ais-Hits-item")
        for producto in productos:
            marca = obtener_texto2(producto, './/div[contains(@class,"product-card_description-wrapper")]/div/span[1]')
            descripcion = obtener_texto2(producto, './/div[contains(@class,"product-card_description-wrapper")]/div/span[2]')    
            promo = obtener_texto(producto, "product-card__sale-price")
            precio = obtener_texto(producto, "reference-price__price")
            precio2 = obtener_texto(producto, "regular-unit-price__price-product-card")
            imagen = obtener_atributo(producto, './/img[@id="lazy-img"]', "src")
            disponibilidad = obtener_texto2(producto, './/span[contains(@class, "Tag-module_tag__3t5NV") and contains(@class, "Tag-module_blue__24bf6") and contains(@class, "Tag-module_secondary__17MMS")]')
            link = obtener_atributo(producto, './/a[@data-testid="product-card-nav-test-id"]', "href")

            info.append({"Supermercado":supermercado, "Semana":semana_actual,"Fecha":dia_actual,"Marca":marca,"Descripcion":descripcion,"Promo":promo,"Precio":precio,"Precio2":precio2,"Imagen":imagen,"Disponibilidad":disponibilidad,"Link":link})

    # Intenta avanzar a la siguiente página
        try:
            boton_siguiente = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/ul/li[6]')
            boton_siguiente.click()
            time.sleep(5)  # Añade una espera para asegurar que la nueva página se haya cargado
            pagina_actual += 1
        except (NoSuchElementException, ElementClickInterceptedException):
            print('No hay más páginas para procesar.')
            break  # Sal del bucle si no hay más páginas o si el botón no es clickeable
    
    nombre_archivo = 'C:/Users/man27/Desktop/AI_test/UL_DW/data_lider.csv'

    # Abre (o crea) el archivo CSV en modo escritura ('w')
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
        # Define el escritor CSV y especifica los nombres de las columnas usando el método DictWriter
        writer = csv.DictWriter(file, fieldnames=["Supermercado","Semana","Fecha","Marca", "Descripcion", "Promo", "Precio", "Precio2", "Imagen", "Disponibilidad", "Link"])
        # Si es la primera vez que se escribe en el archivo o si el archivo está vacío, escribe la fila de encabezado
        if file.tell() == 0:
            writer.writeheader()

        # Itera sobre cada item en la lista 'info' y escribe cada fila en el archivo CSV
        for item in info:
            writer.writerow(item)
            
    # Cierra el WebDriver
    driver.quit()
    print(info)
if __name__ == "__main__":
    run()