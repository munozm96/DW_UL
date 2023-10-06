
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
website = 'https://www.unimarc.cl/category/limpieza/bano-y-cocina/lavalozas-y-lavavajillas'  # Asegúrate de que esta URL sea la correcta
driver.get(website)
time.sleep(10)

fecha_actual = datetime.datetime.now()
semana_actual = fecha_actual.strftime("%U")
dia_actual = fecha_actual.strftime("%d-%m-%Y")
#hora_actual = datetime.datetime.now().strftime('%H:%M:%S')

supermercado ="Unimarc"

info=[]

productos = driver.find_elements(By.XPATH,'//*[@id="__next"]/div/main/div/div/div/div[8]/div/div')
for producto in productos:
    marca = obtener_texto(producto, "Shelf_brandText__sGfsS")
    descripcion = obtener_texto2(producto, './/p[contains(@class,"Shelf_nameProduct__CXI5M ")]')   
    Unidades= obtener_texto2(producto, './/label[contains(@class,"Text_text--right__CHf3V ")]') 
    promo = obtener_texto2(producto, './/p[contains(@class,"Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--medium__rIScp Text_text--xl__l05SR Text_text--primary__OoK0C Text_text__cursor--auto__cMaN1 Text_text--none__zez2n")]')
    precio = obtener_texto(producto, 'Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--medium__rIScp Text_text--md__H7JI_ Text_text--black__zYYxI Text_text__cursor--auto__cMaN1 Text_text--none__zez2n')
    imagen = obtener_atributo(producto, './/img[@id="lazy-img"]', "src")
    disponibilidad = obtener_texto2(producto, './/span[contains(@class, "Tag-module_tag__3t5NV") and contains(@class, "Tag-module_blue__24bf6") and contains(@class, "Tag-module_secondary__17MMS")]')
    link = obtener_atributo(producto, './/a[@data-testid="product-card-nav-test-id"]', "href")

    info.append({"Supermercado":supermercado, "Semana":semana_actual,"Fecha":dia_actual,"Marca":marca,"Descripcion":descripcion,"Promo":promo,"Precio":precio,"Imagen":imagen,"Disponibilidad":disponibilidad,"Link":link})


nombre_archivo = 'C:/Users/man27/Desktop/AI_test/UL_DW/data_unimarc.csv'

# Abre (o crea) el archivo CSV en modo escritura ('w')
with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
    # Define el escritor CSV y especifica los nombres de las columnas usando el método DictWriter
    writer = csv.DictWriter(file, fieldnames=["Supermercado","Semana","Fecha","Marca", "Descripcion", "Promo", "Precio", "Imagen", "Disponibilidad", "Link"])
    # Si es la primera vez que se escribe en el archivo o si el archivo está vacío, escribe la fila de encabezado
    if file.tell() == 0:
        writer.writeheader()

    # Itera sobre cada item en la lista 'info' y escribe cada fila en el archivo CSV
    for item in info:
        writer.writerow(item)
        
# Cierra el WebDriver
driver.quit()
print(info)
