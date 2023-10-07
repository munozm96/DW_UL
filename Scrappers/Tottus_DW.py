
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run():
    def obtener_texto(elemento, clase):
        try:
            return elemento.find_element(By.CLASS_NAME, clase).text
        except NoSuchElementException:
            return ""

    def obtener_atributo(elemento, xpath, atributo):
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
            return elemento.find_element(By.XPATH, xpath).get_attribute(atributo)
        except NoSuchElementException:
            return ""
      
    # Inicia el WebDriver
    driver_service = Service(executable_path="C:\\Users\\man27\\Desktop\\AI_test\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    # Navega a la página web
    website = 'https://tottus.falabella.com/tottus-cl/category/CATG10625/Lavalozas-y-Lava-Vajillas?&f.product.L2_category_paths=CATG10598%7C%7CAseo+y+limpieza%2FCATG10277%7C%7CLavalozas+y+Limpiadores%2FCATG10625%7C%7CLavalozas+y+Lava+Vajillas&store=tottus&subdomain=tottus'  # Asegúrate de que esta URL sea la correcta
    driver.get(website)
    time.sleep(10)

    fecha_actual = datetime.datetime.now()
    semana_actual = fecha_actual.strftime("%U")
    dia_actual = fecha_actual.strftime("%d-%m-%Y")

    supermercado ="Tottus"

    info=[]

    productos = driver.find_elements(By.CLASS_NAME,"jsx-200723616")
    for producto in productos:
        marca = obtener_texto(producto, "pod-title")
        descripcion = obtener_texto(producto, "pod-subTitle")
        promo = obtener_texto(producto, "pod-prices")
        precio = obtener_texto(producto, "copy3")
        imagen = obtener_atributo(producto, ".//descendant::img", "src")
        link = obtener_atributo(producto, ".//ancestor::a", "href")
        info.append({"Supermercado":supermercado, "Semana":semana_actual,"Fecha":dia_actual,"marca":marca,"descripcion":descripcion,"promo":promo,"precio":precio,"imagen":imagen, "Link":link})


    nombre_archivo = 'C:/Users/man27/Desktop/AI_test/UL_DW/Data/data_tottus.csv'

    # Abre (o crea) el archivo CSV en modo escritura ('w')
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
        # Define el escritor CSV y especifica los nombres de las columnas usando el método DictWriter
        writer = csv.DictWriter(file, fieldnames=["Supermercado","Semana","Fecha","marca", "descripcion", "promo", "precio", "imagen","Link"])

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