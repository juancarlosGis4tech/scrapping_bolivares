import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
import matplotlib.pyplot as plt
load_dotenv()
import sqlalchemy
import matplotlib.ticker as ticker

try:
    engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://juancarlos_gq@gis4techazure:'+ os.getenv("PASSWORD")+'@gis4techazure.postgres.database.azure.com:5432/gis4tech',
            connect_args={'connect_timeout': 10}
        )
except Exception as e:
    print("Error al crear el motor", e)

# URL de la página web que contiene el enlace al archivo Excel
url = 'https://datosmacro.expansion.com/divisas/venezuela'

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar los elementos <div> que contienen el enlace al archivo Excel
    divs = soup.find_all('div', {'class': 'dialog-off-canvas-main-canvas'})
else:
    print("Error")

for div in divs:
    # Buscar elementos con clase 'row'
    rows = div.find_all('div', {'class': 'main-container container js-quickedit-main-content'})
    for row in rows:
        # Buscar elementos con clase 'col-md-3 col-xs-6' dentro de cada 'row'
        col_elements = row.find_all('div', {'class': 'row'})
        for class_section in col_elements:
            # Buscar elementos con clase 'excel' dentro de 'col-md-3 col-xs-6'
            excel_elements = class_section.find_all('section', {'class': 'col-sm-8 col-sm-8-asd'})

            for class_section in excel_elements:
                # Buscar elementos con clase 'excel' dentro de 'col-md-3 col-xs-6'
                excel_elements_1 = class_section.find_all('div', {'class': 'region region-content'})

                for class_section in excel_elements_1:
                # Buscar elementos con clase 'excel' dentro de 'col-md-3 col-xs-6'
                    excel_elements_2 = class_section.find_all('article', {'class': 'stat2 full clearfix'})

                    for class_section in excel_elements_2:
                # Buscar elementos con clase 'excel' dentro de 'col-md-3 col-xs-6'
                        excel_elements_3 = class_section.find_all('div', {'class': 'content'})
                        for class_section in excel_elements_3:
                            excel_elements_4 = class_section.find_all('div', {'class': 'tab-content col-sm-12'})

                            for class_section in excel_elements_4:
                                excel_elements_5 = class_section.find_all('div', {'id': 'divus'})

                                for class_section in excel_elements_5:
                                    excel_elements_6 = class_section.find_all('div', {'class': 'row'})
                                    for class_section in excel_elements_6:
                                        excel_elements_7 = class_section.find_all('div', {'class': 'col-sm-5'})
                                        for class_section in excel_elements_7:
                                            excel_elements_8 = class_section.find_all('div', {'class': 'table-responsive'})

datos_tabla = []


for tabla in excel_elements_8:
    # Obtener todas las filas de la tabla
    filas = tabla.find_all("tr")
    
    # Iterar sobre las filas de la tabla
    for fila in filas:
        # Obtener todas las celdas de la fila
        celdas = fila.find_all(["th", "td"])  # Se buscan tanto th (encabezados) como td (celdas de datos)
        
        # Inicializar una lista vacía para almacenar los datos de la fila
        datos_fila = []
        
        # Iterar sobre las celdas de la fila
        for celda in celdas:
            # Agregar el texto de la celda a la lista de datos de la fila
            datos_fila.append(celda.get_text(strip=True))  # strip=True para eliminar espacios en blanco alrededor del texto
        
        # Agregar los datos de la fila a la lista de datos de la tabla
        datos_tabla.append(datos_fila)

nombres_columnas = ["fecha", "cambio", "variacion"]

# Convertir datos_tabla en un DataFrame de pandas con nombres de columnas personalizados
datos_tabla_sin_extremos = datos_tabla[1:-1]

df_tabla = pd.DataFrame(datos_tabla_sin_extremos, columns=nombres_columnas)
df_tabla['fecha'] = pd.to_datetime(df_tabla['fecha'], format='%d/%m/%Y')

fechas = pd.read_sql("SELECT MAX(fecha) from venezuela.venezuela_cambio_bolivar", engine)
fecha = fechas["max"].iloc[0]

df_final = df_tabla[df_tabla["fecha"] > fecha]
print("Se añade", df_final)
df_final.to_sql('venezuela_cambio_bolivar', engine, schema='venezuela', index=False, if_exists='append')

