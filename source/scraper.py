# Usamos 'undetected_chromedriver' en vez del webdriver de selenium por defecto
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
import re

class EngelAndVolkersScraper:
    def __init__(self, url, driver):
        self.mainUrl = url
        self.driver = driver
    
    def _get_page(self, url): 
        sleep(randint(2,5))
        self.driver.get(url)
        
    def _get_item_links(self):
        return [link.get_attribute('href') for link in self.driver.find_elements(By.XPATH, "//a[@class='ev-property-container']")]
    
    def _get_next_page(self):
        try:
            return driver.find_element(By.CLASS_NAME, 'ev-pager-next').get_attribute('href')
        except NoSuchElementException:
            return None
    
    def _build_house(self):
        title = self.driver.find_element(By.XPATH, "//h1[@class='ev-exposee-title ev-exposee-headline']").text
        subtitle = self.driver.find_element(By.XPATH, "//div[@class='ev-exposee-content ev-exposee-subtitle']").text
        
        # Elementos principales de la vivienda
        feature_titles = [title.text.lower() for title in self.driver.find_elements(By.XPATH, "//div[@class='ev-key-fact-title']") if title.is_displayed()]
        feature_values = [value.text for value in self.driver.find_elements(By.XPATH, "//div[@class='ev-key-fact-value']") if value.is_displayed()]

        # Detalles a tener en cuenta de la vivienda
        feature_detail_titles = [title.text.lower() for title in self.driver.find_elements(By.XPATH, "//label[@class='ev-exposee-detail-fact-key']")]
        feature_detail_values = [value.text for value in self.driver.find_elements(By.XPATH, "//span[@class='ev-exposee-detail-fact-value']")]
        
        n_rooms, n_bathrooms, price, area, land, units = None, None, None, None, None, None
        for i in range(len(feature_titles)):
            element_title, element_value = feature_titles[i], feature_values[i]
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

        
        print(title,subtitle)
        print(feature_detail_titles)
        print(feature_detail_values)
        print("--------------")
        
    def get_data(self):
        i = 0
        pageToExplore = self.mainUrl
        links = self._get_item_links()
        while pageToExplore != None:
            if (i == 1):
                break
            self._get_page(pageToExplore)
            
            if (pageToExplore == self.mainUrl):
                try:
                    disagreeProcessingDataBtn = self.driver.find_element(By.XPATH, "//button[@id='didomi-notice-disagree-button']")
                    disagreeProcessingDataBtn.click()
                except NoSuchElementException:
                    pass
            
            links = links + self._get_item_links()
            pageToExplore = self._get_next_page()
            i += 1
        houses = list()
        for link in links:
            self._get_page(link)
            house = self._build_house()
        driver.close()

if __name__ == '__main__':
    target_url = "https://www.engelvoelkers.com/es/search/?q=&startIndex=0&businessArea=residential&sortOrder=DESC&sortField=sortPrice&pageSize=18&facets=bsnssr%3Aresidential%3Bcntry%3Aspain%3Brgn%3Abarcelona%3Btyp%3Abuy%3B"
    driver = uc.Chrome(use_subprocess=True)
    userAgent = driver.execute_script("return navigator.userAgent")
    print("User-Agent:",userAgent)
    eav = EngelAndVolkersScraper(target_url, driver)
    eav.get_data()