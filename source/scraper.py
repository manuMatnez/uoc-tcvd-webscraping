# Usamos 'undetected_chromedriver' en vez del webdriver de selenium por defecto
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
import re

 # 
 # This file is part of the practice 1 of the Tipología y ciclo de vida de los datos
 # this is a subject of the Master's degree called Data Science
 # Copyright (c) 2023 Manuel Ernesto Martínez Martín, Vanessa Moreno Gonzalez.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

"""
Universitat Oberta de Catalunya: Tipología y ciclo de vida de los datos

Autores: Manuel Ernesto Martínez Martín, Vanessa Moreno Gonzalez

EngelAndVolkersScraper: Extrae la información de viviendas de EneglAndVolkers de una zona concreta y genera un archivo csv
"""
class EngelAndVolkersScraper:
    def __init__(self, url, driver):
        self.mainUrl = url
        self.driver = driver    

    """
    Carga la página que se desea aplicar scraping, se aplica un delay aleatorio de entre 2 y 5 segundos
    @Params url : <String>
    @Return void
    """
    def _get_page(self, url): 
        sleep(randint(2,5))
        self.driver.get(url)

    """
    Obtiene los enlaces de las viviendas de la página que está actualmente cargada usando list comprehension
    Se utiliza el XPATH para obtener los enlaces y un get_attribute() para obtener el enlace como texto
    @Return: list<String>
    """
    def _get_item_links(self):
        return [link.get_attribute('href') for link in self.driver.find_elements(By.XPATH, "//a[@class='ev-property-container']")]
    
    """
    Obtiene el enlace de la próxima página a la que hay que hacer scraping
    Se hace por el @class del html, una vez se obtiene el enlace con get_attribute() se retorna
    Si no hay ninguna página más (no existe enlace de 'siguiente') se retorna None
    @Return: String / None
    """
    def _get_next_page(self):
        try:
            return driver.find_element(By.CLASS_NAME, 'ev-pager-next').get_attribute('href')
        except NoSuchElementException:
            return None

    """
    Se hace scraping en la web de la vivienda cargada para sacar los atributos necesarios para generar el csv
    En este caso los datos estan un poco segmentados básicamente tienen etiquetas por resumirlo: de clave valor
    Hay dos listas de claves y dos listas de valores, una es de la cabecera de la casa y otra de los detalles extras
    Con lo cual se tendran listas de claves y listas de valores en als que debe de haber la misma dimensión
    Se comprueba con REGEX cada elemento de cada lista de 'claves' y se coge el valor del mismo indice y se guarda en variable
    @Return: FIXME
    """
    def _build_house(self):
        # Nombre de la vivienda
        title = self.driver.find_element(By.XPATH, "//h1[@class='ev-exposee-title ev-exposee-headline']").text

        # Información adicional al nombre de la vivienda
        subtitle = self.driver.find_element(By.XPATH, "//div[@class='ev-exposee-content ev-exposee-subtitle']").text
        
        # Elementos principales en la cabecera de la información de la vivienda
        # Son los acompañados de icono y texto
        feature_head_titles = [title.text.lower() for title in self.driver.find_elements(By.XPATH, "//div[@class='ev-key-fact-title']") if title.is_displayed()]
        feature_head_values = [value.text for value in self.driver.find_elements(By.XPATH, "//div[@class='ev-key-fact-value']") if value.is_displayed()]
        
        n_rooms, n_bathrooms, price, area, land, units = None, None, None, None, None, None
        for i in range(len(feature_head_titles)):
            element_title, element_value = feature_head_titles[i], feature_head_values[i]
            if (re.match("^(dormitorios|cuartos)$", element_title)):
                n_rooms = element_value
            elif (re.match("^(baños)$", element_title)):
                n_bathrooms = element_value
            elif (re.match("^(precio)$", element_title)):
                price = element_value
            elif (re.match("^(superficie habitable aprox.|superficie construida aprox.)$", element_title)):
                area = element_value
            elif (re.match("^terreno aprox.$", element_title)):
                land = element_value
            elif (re.match("^unidades residenciales$", element_title)):
                units = element_value

        # Detalles a tener en cuenta de la vivienda, hay algunos valores que coinciden con los de cabecera
        # Están más abajo y tienen un título similar a 'LO QUE TIENE QUE SABER SOBRE'
        feature_detail_titles = [title.text.lower() for title in self.driver.find_elements(By.XPATH, "//label[@class='ev-exposee-detail-fact-key']")]
        feature_detail_values = [value.text for value in self.driver.find_elements(By.XPATH, "//span[@class='ev-exposee-detail-fact-value']")]

        
        print(title,subtitle)
        print(feature_detail_titles)
        print(feature_detail_values)
        print("--------------")
    
    """
    Declina el uso de cookies de la página web
    Utiliza XPATH para localizar el componente de botón que declina
    @Return: void
    """
    def _decline_cookies(self):
        try:
            disagreeProcessingDataBtn = self.driver.find_element(By.XPATH, "//button[@id='didomi-notice-disagree-button']")
            disagreeProcessingDataBtn.click()
        except NoSuchElementException:
            pass
        
    """
    Se encarga de ir sacando todos los enlaces de todas las páginas de viviendas de EngelAndVolkers para una ubicación
    Dichos enlaces de almacenan en una lista local para posteriormente recorrela
    En la primera iteración se ha de aceptar/declinar las cookies
    Después se ha de ir recorriendo de uno en uno para hacer scraping de cada vivienda y escribir en un archivo csv
    @Return: void
    """
    def get_data(self):
        i = 0
        pageToExplore = self.mainUrl
        links = self._get_item_links()
        while pageToExplore != None:
            if (i == 1):
                break
            self._get_page(pageToExplore)
            
            if (pageToExplore == self.mainUrl):
                self._decline_cookies()
            
            links = links + self._get_item_links()
            pageToExplore = self._get_next_page()
            i += 1
        houses = list()
        for link in links:
            self._get_page(link)
            house = self._build_house()
        self.driver.close()

"""
Programa principal
Se indica la URL de EngelAndVolkers con el municipio
Se carga el webdriver, se imprime el User-Agent y se inicia el wescraping
"""
if __name__ == '__main__':
    target_url = "https://www.engelvoelkers.com/es/search/?q=&startIndex=0&businessArea=residential&sortOrder=DESC&sortField=sortPrice&pageSize=18&facets=bsnssr%3Aresidential%3Bcntry%3Aspain%3Brgn%3Abarcelona%3Btyp%3Abuy%3B"
    driver = uc.Chrome(use_subprocess=True)
    userAgent = driver.execute_script("return navigator.userAgent")
    print("User-Agent:",userAgent)
    eav = EngelAndVolkersScraper(target_url, driver)
    eav.get_data()