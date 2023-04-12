# Práctica 1: Viviendas de lujo en venta de E & V en Barcelona [UOC - Tipología y ciclo de vida de los datos aula 1]

## Descripción

Este proyecto ha sido desarrollado para la asignatura de **Tipología y ciclo de vida de los datos** del máster de **Ciencia de Datos** de la **Universitat Oberta de Catalunya** y tiene como objetivo recopilar datos sobre el sector inmobiliario de lujo en la provincia de Barcelona, reuniendo información de las características de los inmuebles en venta, como pueden ser la ubicación, el tamaño o la antigüedad, entre otros, que pueden influir en su precio de venta. Estos datos, se emplearán para crear modelos predictivos que permitan estimar el precio de las viviendas en función de sus características.

El dataset contiene información de **2105 viviendas de lujo**, en venta, disponibles en la provincia de Barcelona. La información incluida en este dataset es una recopilación de **25 características de las propiedades**, como son el número de habitaciones, el tipo de inmueble, el número de baños, el barrio donde ubica, el año de construcción, el estado del inmueble y la descripción, entre otras, así como el precio de venta.

* **Zenodo**: https://zenodo.org/record/7823310#.ZDbmcS9j6_I

* **DOI**: 10.5281/zenodo.7823310

### Variables

id, eav_id, title, subtitle, n_rooms, n_bedrooms, n_bathrooms, useful_area, built_area, land_area, price, built_year, energy_class, energy_consumption, co2_emission, co2_emission_scale, protected, status, parking, garage, floor_cover, property_subclass, terrace_area, heating_type, location_status

## Miembros del equipo

La actividad ha sido realizada por: **Vanessa Moreno González** y **Manuel Ernesto Martínez Martín**.

## Ficheros del código fuente

* **source/scraper.py**: Es el punto de entrada al programa. Inicia el proceso de scraping y además contiene la implementación de la clase _EngelAndVolkersScraper_ cuyos métodos generan el conjunto de datos a partir de la web inmobiliaria de viviendas de lujo [Engel&Volkers](https://www.engelvoelkers.com/es/) para viviendas de la provincia de Barcelona.

## Ficheros que no son parte del código

* **requirements.txt**: Librerias junto a sus versiones, necesario para ejecutar el proyecto.
* **LICENSE.txt**: Licencia del proyecto (GNU v3.0).
* **README.md**: Información del repositorio y del proyecto.
* **dataset/Viviendas_de_lujo_en_venta_de_E&V_en_Barcelona.csv**: Dataset de las viviendas extraido con el script de Python en engelandvolkers.
* **.gitignore**: Evita que se suban archivos del sistema operativo al repositorio.

## Licencia

**GNU General Public License v3.0**

La razón principal para elegir esta licencia es que se trata de una licencia de software libre y código abierto y permite que los usuarios de éste, puedan libremente usar, estudiar y compartir este dataset. Esta licencia es tipo copyleft, que garantiza que la distribución de estos datos se haga bajo esta misma licencia.

## Información adicional

* Si toda la ejecución va bien, se generá un archivo csv de viviendas con el nombre "_eav_houses_TIMESTAMP.csv_".
* Si algún enlace a consultar falla, se genera otro csv que puede ser adicional al csv de viviendas o único con el siguiente nombre "_errors_TIMESTAMP.csv_".
* Los requisitos han sido generados con '**pipreqs**' en lugar de 'pip freeze'

## Recursos

Subirats Maté, L. y Calvo González, M. (2019). Web Scraping [Material Digital].Tipología y ciclo de vida de los datos . Universidad Oberta de Catalunya.
