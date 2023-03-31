# Usamos 'undetected_chromedriver' en vez del webdriver de selenium por defecto
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint

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
        sleep(randint(1,3))
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
        
        house = {
            "eav_id": None,
            "n_rooms": None,
            "n_bedrooms": None,
            "n_bathrooms": None,
            "price": None,
            "useful_area": None,
            "built_area": None,
            "land_area": None,
            "built_year": None,
            "units": None,
            "heating_type": None,
            "location_status": None,
            "energy_class": None,
            "energy_consumption": None,
            "co2_emission": None,
            "co2_emission_scale": None,
            "parking": None,
            "status": None,
            "vpo": False,
            "terrace_area": None,
            "floor_cover": None,
            "porperty_subclass": None
        }

        # Variables de la cabecera de la vivienda (algunas estan en detalles también)
        for i in range(len(feature_head_titles)):
            element_title, element_value = feature_head_titles[i], feature_head_values[i]
            if ("cuartos" == element_title):
                house['n_rooms'] = element_value
            if ("dormitorios" == element_title):
                house['n_bedrooms'] = element_value
            elif ("baños" == element_title):
                house['n_bathrooms'] = element_value
            elif ("precio" == element_title):
                house['price'] = element_value
            elif ("superficie habitable aprox." == element_title):
                house['useful_area'] = element_value
            elif ("superficie construida aprox." == element_title):
                house['built_area'] = element_value
            elif ("terreno aprox." == element_title):
                house['land_area'] = element_value
            elif ("unidades residenciales" == element_title):
                house['units'] = element_value

        # Detalles a tener en cuenta de la vivienda, hay algunos valores que coinciden con los de cabecera
        # Están más abajo y tienen un título similar a 'LO QUE TIENE QUE SABER SOBRE'
        # Algunos parámetros como habitaciones, baños o superficies se pueden rescatar de aquí si faltaran en la cabecera pero aquí no
        
        feature_detail_titles = [title.text.lower() for title in self.driver.find_elements(By.XPATH, "//div[@class='ev-exposee-detail']/ul[@class='ev-exposee-content ev-exposee-detail-facts ']/li[@class='ev-exposee-detail-fact']/label[@class='ev-exposee-detail-fact-key']")]
        feature_detail_values = [value.text for value in self.driver.find_elements(By.XPATH, "//div[@class='ev-exposee-detail']/ul[@class='ev-exposee-content ev-exposee-detail-facts ']/li[@class='ev-exposee-detail-fact']/span[@class='ev-exposee-detail-fact-value']")]

        print("33333333333")
        print(feature_detail_titles)
        print("22222222222")
        print(feature_detail_values)
        print("33333333333")
        print("\n")

        for i in range(len(feature_detail_titles)):
            detail_element_title, detail_element_value = feature_detail_titles[i], feature_detail_values[i]
            # POSIBLES REPETIDOS
            if ("cuartos" == detail_element_title and house['n_rooms'] == None):
                house['n_rooms'] = detail_element_value
            if ("dormitorios" == detail_element_title and house['n_bedrooms'] == None):
                house['n_bedrooms'] = detail_element_value
            elif ("baños" == detail_element_title and house['n_bathrooms'] == None):
                house['n_bathrooms'] = detail_element_value
            elif ("superficie habitable aprox." == detail_element_title and house['useful_area'] == None):
                house['useful_area'] = detail_element_value
            elif ("superficie construida aprox." == detail_element_title and house['built_area'] == None):
                house['built_area'] = detail_element_value
            elif ("terreno aprox." == detail_element_title and house['land_area'] == None):
                house['land_area'] = detail_element_value
            # NO REPETIDOS
            elif ("e&v id" == detail_element_title):
                house['eav_id'] = detail_element_value
            elif ("año de construcción" == detail_element_title):
                house['built_year'] = detail_element_value
                print("TEST")
                print(i, detail_element_title, detail_element_value)
            elif ("clase de eficiencia energética" == detail_element_title):
                house['energy_class'] = detail_element_value
            elif ("valor de consumo energético" == detail_element_title):
                house['energy_consumption'] = detail_element_value
            elif ("co2 emission" == detail_element_title):
                house['co2_emission'] = detail_element_value
            elif ("escala de emisiones de co2" == detail_element_title):
                house['co2_emission_scale'] = detail_element_value
            elif ("edificio protegido" == detail_element_title):
                house['vpo'] = True
            elif ("estado" == detail_element_title):
                house['status'] = detail_element_value
            # Una casa tiene o parking o garage
            elif ("parking" == detail_element_title or "garaje" == detail_element_title):
                house['parking'] = detail_element_value
            elif ("revestimiento del suelo" == detail_element_title):
                house['floor_cover'] = detail_element_value
            elif ("subclase de la propiedad" == detail_element_title):
                house['porperty_subclass'] = detail_element_value
            elif ("terraza" == detail_element_title):
                house['terrace_area'] = detail_element_value
            elif ("tipo de calefacción" == detail_element_title):
                house['heating_type'] = detail_element_value
            elif ("ubicación" == detail_element_title):
                house['location_status'] = detail_element_value

            
        
        #print(title,subtitle)
        #print(feature_detail_titles)
        #print(feature_detail_values)
        print("------",title,"--------")
        return house
    
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
    Navega por cada p´gina de la busqueda de viviendas, en cada página se extraen los links de las viviendas
    En la primera iteración se ha de aceptar/declinar las cookies
    @Return: void
    """
    def get_data(self):
        i = 0
        nextPage = self.mainUrl
        while nextPage != None:
            if (i == 2):
                break
            self._get_page(nextPage)

            if (nextPage == self.mainUrl):
                self._decline_cookies()
            nextPage = self._get_next_page()

            for link in self._get_item_links():
                self._get_page(link)
                tmp = self._build_house()
                print(tmp)

            i += 1
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