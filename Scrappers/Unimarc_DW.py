
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
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        
    def check_loading_animation(driver):
        # Reemplaza 'tu_selector' con el selector apropiado para las animaciones de carga
        loading_animations = driver.find_elements(By.CSS_SELECTOR, 'tu_selector')  
        return len(loading_animations) == 0

    # Inicia el WebDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver_service = Service(executable_path="C:\\Users\\man27\\Desktop\\AI_test\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service,options=options)
    # Navega a la página web
    website = 'https://www.unimarc.cl/category/limpieza/bano-y-cocina/lavalozas-y-lavavajillas'  # Asegúrate de que esta URL sea la correcta
    driver.get(website)
    time.sleep(10)

    fecha_actual = datetime.datetime.now()
    semana_actual = fecha_actual.strftime("%U")
    dia_actual = fecha_actual.strftime("%d-%m-%Y")
    #hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    wait = WebDriverWait(driver, 20)  # espera hasta 10 segundos antes de lanzar una excepción
    wait.until(lambda driver: check_loading_animation(driver))
    supermercado ="Unimarc"

    info=[]

    productos = driver.find_elements(By.CSS_SELECTOR,".baseContainer_container__TSgMX.ab__shelves.abc__shelves.baseContainer_justify-start___sjrG.baseContainer_align-start__6PKCY.baseContainer_absolute-default--topLeft__lN1In")
    for producto in productos:
        marca = obtener_texto(producto, "Shelf_brandText__sGfsS")
        descripcion = obtener_texto2(producto, './/p[contains(@class,"Shelf_nameProduct__CXI5M ")]')   
        Unidades = obtener_texto2(producto, './/label[contains(@class,"Text_text--right__CHf3V")]')
        promo = obtener_texto2(producto, './/p[contains(text(), "$")]')
        precio = obtener_texto2(producto, './/p[contains(@class, "Text_text--line-through__1V_2e")]')
        precio2 = obtener_texto2(producto, './/p[contains(@class, "Text_text__cB7NM") and contains(@class, "Text_text--black__zYYxI") and contains(@class, "Text_text__cursor--auto__cMaN1")]')
        imagen = obtener_atributo(producto, './/img', "src")
        link = obtener_atributo(producto, './/a', "href")

        info.append({"Supermercado":supermercado, "Semana":semana_actual,"Fecha":dia_actual,"Marca":marca,"Descripcion":descripcion,"Unidades":Unidades,"Promo":promo,"Precio":precio,"Precio2":precio2,"Imagen":imagen,"Link":link})

    nombre_archivo = 'C:/Users/man27/Desktop/AI_test/UL_DW/Data/data_unimarc.csv'

    # Abre (o crea) el archivo CSV en modo escritura ('w')
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
        # Define el escritor CSV y especifica los nombres de las columnas usando el método DictWriter
        writer = csv.DictWriter(file, fieldnames=["Supermercado","Semana","Fecha","Marca", "Descripcion", "Unidades","Promo", "Precio","Precio2", "Imagen", "Link"])
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