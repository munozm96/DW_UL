
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
import datetime
from selenium.common.exceptions import ElementClickInterceptedException


def run():
    def obtener_texto(elemento, clase):
        try:
            return elemento.find_element(By.CLASS_NAME, clase).text
        except NoSuchElementException:
            return ""

    def obtener_atributo(elemento, clase, atributo):
        try:
            return elemento.find_element(By.CLASS_NAME, clase).get_attribute(atributo)
        except NoSuchElementException:
            return ""
        
    def obtener_codigo():
        try:
            elemento_codigo = driver.find_element(By.XPATH, '//span[contains(@class,"product-code")]/text()[2]')
            return elemento_codigo.text
        except NoSuchElementException:
            return ""

    # Inicia el WebDriver
    driver_service = Service(executable_path="C:\\Users\\man27\\Desktop\\AI_test\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    # Navega a la página web
    website = 'https://www.santaisabel.cl/limpieza/bano-y-cocina/lavalozas'  # Asegúrate de que esta URL sea la correcta
    driver.get(website)
    time.sleep(10)


    pagina_actual = 1# Asume que la primera página es 1
    max_paginas = 1 #usta este valor al número máximo de páginas que deseas procesar

    fecha_actual = datetime.datetime.now()
    semana_actual = fecha_actual.strftime("%U")
    dia_actual = fecha_actual.strftime("%d-%m-%Y")

    supermercado ="Santa Isabel"

    info=[]
    while pagina_actual <= max_paginas:
        productos = driver.find_elements(By.CLASS_NAME,"product-card")
        for producto in productos:
            marca = obtener_texto(producto, "product-card-brand")
            descripcion = obtener_texto(producto, "product-card-name")
            promo = obtener_texto(producto, "prices-main-price")
            precio = obtener_texto(producto, "prices-old-price")
            imagen = obtener_atributo(producto, "lazy-image ", "src")
            promo_exclusiva = obtener_texto(producto, "price-box")
            link = obtener_atributo(producto, "product-card-image-link", "href")
            info.append({"Supermercado":supermercado, "Semana":semana_actual,"Fecha":dia_actual,"marca":marca,"descripcion":descripcion,"promo":promo,"precio":precio,"imagen":imagen,"promo_exclusiva":promo_exclusiva,"link":link})

    # Intenta avanzar a la siguiente página
        try:
            boton_siguiente = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div/main/div[3]/div[2]/div[2]/div[2]/button[2]')
            boton_siguiente.click()
            time.sleep(5)  # Añade una espera para asegurar que la nueva página se haya cargado
            pagina_actual += 1
        except (NoSuchElementException, ElementClickInterceptedException):
            print('No hay más páginas para procesar.')
        break  # Sal del bucle si no hay más páginas o si el botón no es clickeable
    nombre_archivo = 'C:/Users/man27/Desktop/AI_test/UL_DW/Data/data_sisa.csv'

    # Abre (o crea) el archivo CSV en modo escritura ('w')
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
        # Define el escritor CSV y especifica los nombres de las columnas usando el método DictWriter
        writer = csv.DictWriter(file, fieldnames=["Supermercado","Semana","Fecha","marca", "descripcion", "promo", "precio", "imagen", "promo_exclusiva", "link"])

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