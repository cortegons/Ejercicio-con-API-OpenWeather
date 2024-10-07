# Weather Data ETL Automation

Este proyecto ejecuta un script de ETL para obtener datos meteorológicos de 5 ciudades utilizando la API de OpenWeatherMap, los almacena en una base de datos PostgreSQL y genera un archivo CSV con los datos obtenidos.

## Automatización con GitHub Actions

La GitHub Action configurada en `.github/workflows/weather_data.yml` ejecuta diariamente el script de ETL para recopilar los datos meteorológicos y generar un archivo CSV. El archivo se sube automáticamente al repositorio después de cada ejecución diaria.

### Cómo funciona:

1. La GitHub Action se ejecuta diariamente a las 00:00 UTC.
2. El script `weather_etl.py` recopila los datos de la API de OpenWeatherMap.
3. Los datos se guardan en un archivo CSV llamado `weather_data.csv`.
4. El archivo CSV es subido automáticamente al repositorio después de la ejecución.

### Requisitos

- Python 3.9
- Dependencias indicadas en el archivo `requirements.txt`.

