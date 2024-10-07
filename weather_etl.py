import requests
import logging
import os
import time
import csv
from datetime import datetime  # Importa datetime para obtener la fecha y hora

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s',
                    handlers=[
                        logging.FileHandler("weather_etl.log"),
                        logging.StreamHandler()])

# Variables de entorno para la conexión a la base de datos y la API
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST', 'db')  # Nombre del servicio en docker-
db_name = os.getenv('POSTGRES_DB')
api_key = os.getenv('OPENWEATHER_API_KEY')

# Lista de ciudades
cities = ["London", "New York", "Tokyo", "Bogotá", "Paris"]
# cities = ["Bogotá"] Test

# Crear conexión a la base de datos PostgreSQL

# Función para obtener las coordenadas de una ciudad
def get_coordinates(city):
    limit = 1
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        
        if len(data) > 0:
            lat = data[0]['lat']
            lon = data[0]['lon']
            logging.info(f"Coordenadas de {city}: Lat {lat}, Lon {lon}")
            return lat, lon
        else:
            logging.error(f"No se encontraron coordenadas para {city}")
            return None, None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener coordenadas para {city}: {e}")
        return None, None

# Función para obtener los datos del clima usando las coordenadas
def get_weather_data(lat, lon, city):
    if lat is None or lon is None:
        return None
    part = 'minutely,hourly'
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()
        
        # Extraemos la información que nos interesa
        weather_info = {
            'city': city,
            'temperature': data['current']['temp'],
            'humidity': data['current']['humidity'],
            'weather_description': data['current']['weather'][0]['description'],
            'wind_speed': data['current']['wind_speed']
        }
        logging.info(f"Datos obtenidos correctamente para {city}: {weather_info}")
        return weather_info

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener los datos del clima para {city}: {e}")
        return None

# Función para guardar los datos meteorológicos en un archivo CSV
def save_to_csv(weather_data, filename="weather_data.csv"):
    file_exists = os.path.isfile(filename)
    
    # Obtiene la fecha y hora actual
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Añade la fecha y hora a los datos del clima
    weather_data['execution_time'] = execution_time  # Agrega el tiempo de ejecución
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        # Define los nombres de los campos, asegurando que 'execution_time' esté al principio
        fieldnames = ['execution_time'] + list(weather_data.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Si el archivo no existe, escribir el encabezado
        if not file_exists:
            writer.writeheader()
        
        # Escribir los datos
        writer.writerow(weather_data)

# Ejecutar 
for city in cities:
    lat, lon = get_coordinates(city)
    weather_info = get_weather_data(lat, lon, city)
    # insert_weather_data(weather_info)
    save_to_csv(weather_info)
    time.sleep(1)  # Para evitar hacer demasiadas solicitudes en un corto periodo
