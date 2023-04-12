# Usamos 'undetected_chromedriver' en vez del webdriver de selenium por defecto
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from random import randint
import pandas as pd

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
    Carga la página que se desea aplicar scraping, se aplica un delay aleatorio de entre 1 y 3 segundos
    @Param1 url : <String>
    @Return void
    """
    def _get_page(self, url): 
        time.sleep(randint(1,3))
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
    Obtiene el valor de un elemento deseado que puede venir como 'value\nkey' o 'key value'
    @Params item : <String> (texto clave-valor)
    @Param2 column_name : <String> (columna a aplicar el substring)
    @Param3 head : <bool> (cabecero o cuerpo)
    @Return: String
    """
    def _generate_string(self, item, column_name, head=False):
        if (head):
            return item[0:item.index(column_name)]
        else:
            return item[item.index(column_name)+len(column_name)+1:]

    """
    Se hace scraping en la web de la vivienda cargada para sacar los atributos necesarios para generar el csv
    En este caso los datos estan un poco segmentados básicamente tienen etiquetas por resumirlo: de clave valor
    Los elememtos principales de la cabecera tienen el formato 'valor\nclave' y los elementos de los detalles 'clave valor'
    Por tanto se generan dos listas y se aplica substring a ambas siguiendo dos estrategias
    @Return: dict
    """
    def _build_house(self):
        house = {
            "eav_id": None,
            "title": None,
            "subtitle": None,
            "n_rooms": None,
            "n_bedrooms": None,
            "n_bathrooms": None,
            "useful_area": None,
            "built_area": None,
            "land_area": None,
            "price": None,
            "built_year": None,
            "energy_class": None,
            "energy_consumption": None,
            "co2_emission": None,
            "co2_emission_scale": None,
            "protected": None,
            "status": None,
            "parking": None,
            "garage": None,
            "floor_cover": None,
            "property_subclass": None,
            "terrace_area": None,
            "heating_type": None,
            "location_status": None
        }

        # Nombre de la vivienda
        title = self.driver.find_element(By.XPATH, "//h1[@class='ev-exposee-title ev-exposee-headline']").text
        house['title'] = title

        # Información adicional al nombre de la vivienda
        subtitle = self.driver.find_element(By.XPATH, "//div[@class='ev-exposee-content ev-exposee-subtitle']").text
        house['subtitle'] = subtitle

        # Elementos principales en la cabecera de la información de la vivienda
        # Son los acompañados de icono y texto
        feature_head_items = [ item.text.replace("\n", "") for item in self.driver.find_elements(By.XPATH, "//div[contains(@class,'ev-key-facts')]/div[contains(@class,'ev-key-fact')]") if item.is_displayed()]
        for feature_head_item in feature_head_items:
            if ("Cuartos" in feature_head_item):
                house['n_rooms'] =  self._generate_string(feature_head_item, "Cuartos", True)
            elif ("Dormitorios" in feature_head_item):
                house['n_bedrooms'] = self._generate_string(feature_head_item, "Dormitorios", True)
            elif ("Baños" in feature_head_item):
                house['n_bathrooms'] = self._generate_string(feature_head_item, "Baños", True)
            elif ("Precio" in feature_head_item):
                house['price'] = self._generate_string(feature_head_item, "Precio", True)
            elif ("Superficie habitable aprox." in feature_head_item):
                house['useful_area'] = self._generate_string(feature_head_item, "Superficie habitable aprox.", True)
            elif ("Superficie construida aprox." in feature_head_item):
                house['built_area'] = self._generate_string(feature_head_item, "Superficie construida aprox.", True)
            elif ("Terreno aprox." in feature_head_item):
                house['land_area'] = self._generate_string(feature_head_item, "Terreno aprox.", True)
        
        # [not(descendant::*[contains(@class,'ev-exposee-detail-sub-facts')])] impide que se traiga a los hijos, teníamos un problema y es que queremos los ul(ev-exposee-detail-facts)/li(ev-exposee-detail-fact), pero
        # existen otros elementos en la web que usan las mismas clases ul (ev-exposee-detail-facts)/li(ev-exposee-detail-fact) pero que tienen un span/ul/li colgandod e ellos que nos mezclaba el contenido y nos impedía sacar bien la información
        # básicamente se quiere evitar el class ev-exposee-detail-sub-facts de los ancestros
        feature_detail_items = [item.text for item in self.driver.find_elements(By.XPATH, "//ul[contains(@class,'ev-exposee-detail-facts')]/li[contains(@class,'ev-exposee-detail-fact')][not(descendant::*[contains(@class,'ev-exposee-detail-sub-facts')])]") if item]
        for feature_detail_item in feature_detail_items:
            # POSIBLES REPETIDOS
            if ("Cuartos" in feature_detail_item and house['n_rooms'] == None):
                house['n_rooms'] =  self._generate_string(feature_detail_item, "Cuartos")
            elif ("Dormitorios" in feature_detail_item and house['n_bedrooms'] == None):
                house['n_bedrooms'] = self._generate_string(feature_detail_item, "Dormitorios")
            elif ("Baños" in feature_detail_item and house['n_bathrooms'] == None):
                house['n_bathrooms'] = self._generate_string(feature_detail_item, "Baños")
            elif ("Superficie habitable aprox." in feature_detail_item and house['useful_area'] == None):
                house['useful_area'] = self._generate_string(feature_detail_item, "Superficie habitable aprox.")
            elif ("Superficie construida aprox." in feature_detail_item and house['built_area'] == None):
                house['built_area'] = self._generate_string(feature_detail_item, "Superficie construida aprox.")
            elif ("Terreno aprox." in feature_detail_item and house['land_area'] == None):
                house['land_area'] = self._generate_string(feature_detail_item, "Terreno aprox.")

            # NO REPETIDOS
            elif ("E&V ID" in feature_detail_item):
                 house['eav_id'] = self._generate_string(feature_detail_item, "E&V ID")
            elif ("Año de construcción" in feature_detail_item):
                house['built_year'] = self._generate_string(feature_detail_item, "Año de construcción")
            elif ("Clase de eficiencia energética" in feature_detail_item):
                house['energy_class'] = self._generate_string(feature_detail_item, "Clase de eficiencia energética")
            elif ("Valor de consumo energético" in feature_detail_item):
                house['energy_consumption'] = self._generate_string(feature_detail_item, "Valor de consumo energético")
            elif ("CO2 emission" in feature_detail_item):
                house['co2_emission'] = self._generate_string(feature_detail_item, "CO2 emission")
            elif ("Escala de Emisiones de CO2" in feature_detail_item):
                house['co2_emission_scale'] =  self._generate_string(feature_detail_item, "Escala de Emisiones de CO2")
            elif ("Edificio protegido" in feature_detail_item):
                house['protected'] = True
            elif ("Estado" in feature_detail_item):
                house['status'] = self._generate_string(feature_detail_item, "Estado")
            elif ("Parking" in feature_detail_item):
                house['parking'] = self._generate_string(feature_detail_item, "Parking")
            elif ("Garaje" in feature_detail_item):
                house['garage'] = self._generate_string(feature_detail_item, "Garaje")
            elif ("Revestimiento del suelo" in feature_detail_item):
                house['floor_cover'] = self._generate_string(feature_detail_item, "Revestimiento del suelo")
            elif ("Subclase de la propiedad" in feature_detail_item):
                house['property_subclass'] = self._generate_string(feature_detail_item, "Subclase de la propiedad")
            elif ("Terraza" in feature_detail_item):
                house['terrace_area'] = self._generate_string(feature_detail_item, "Terraza")
            elif ("Tipo de calefacción" in feature_detail_item):
                house['heating_type'] = self._generate_string(feature_detail_item, "Tipo de calefacción")
            elif ("Ubicación" in feature_detail_item):
                house['location_status'] = self._generate_string(feature_detail_item, "Ubicación")

        print("-> SCRAPED home: {htitle}".format(htitle = title))
        return house
    
    """
    Crea una entrada de error como JSON
    @Params index : <int> (número de página donde ha fallado)
    @Param2 level : <String> (es página o sub-página)
    @Param3 link : <String> (enlace fallido)
    @Return: dict
    """
    def _build_error(self, index, level, link, exceptionType):
        return {"page_index": index+1, "level": level, "link": link, "exceptionType": exceptionType}

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
    Navega por cada página de la busqueda de viviendas, en cada página se extraen los links de las viviendas
    En la primera iteración se ha de aceptar/declinar las cookies
    @Return: void
    """
    def get_data(self):
        i = 0
        nextPage = self.mainUrl
        errors, houses = [], []
        while nextPage != None:
            try:
                self._get_page(nextPage)
            except Exception as e:
                errors.append(self._build_error(i, "page", nextPage, type(e)))
                print("-> ERROR on page {pagelink} with exception {exceptionType}".format(pagelink = nextPage, exceptionType = type(e)))
                break

            if (nextPage == self.mainUrl):
                self._decline_cookies()
            nextPage = self._get_next_page()

            for link in self._get_item_links():
                try:
                    self._get_page(link)
                    houses.append(self._build_house())
                except Exception as e:
                    errors.append(self._build_error(i, "link", link, type(e)))
                    print("-> ERROR on link {pagelink} with exception {exceptionType}".format(pagelink = link, exceptionType = type(e)))
            i += 1
        if(houses):
            df = pd.DataFrame(houses)
            houses_file_name = "Viviendas_de_lujo_en_venta_de_E&V_en_Barcelona.csv"
            df.to_csv (houses_file_name, index = True)
        if (errors):
            df_errors = pd.DataFrame(errors)
            error_file_name = "errors_{tstamp}.csv".format(tstamp = time.time())
            df_errors.to_csv (error_file_name, index = True)
        self.driver.quit()

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
