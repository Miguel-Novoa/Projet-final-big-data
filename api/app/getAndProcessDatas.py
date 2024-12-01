import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from ..app.models.weather import Station, WeatherData, Year
from models.weather import Station, WeatherData, Year

# Connexion à la base de données
DATABASE_URL = "postgresql://myuser:mypassword@postgres/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base_url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/"

def fetch_and_process_data(year):
    year_url = base_url.format(year=year)
    response = requests.get(year_url)
    
    csv_files = [file for file in response.text.splitlines() if file.endswith(".csv")][:10]

    for csv_file in csv_files:
        process_csv(year, csv_file)

def process_csv(year, csv_file):
    file_url = base_url + csv_file
    df = pd.read_csv(file_url)

    df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')
    df['DEWP'] = pd.to_numeric(df['DEWP'], errors='coerce')
    df['SLP'] = pd.to_numeric(df['SLP'], errors='coerce')
    df['VISIB'] = pd.to_numeric(df['VISIB'], errors='coerce')
    df['WDSP'] = pd.to_numeric(df['WDSP'], errors='coerce')
    df['GUST'] = pd.to_numeric(df['GUST'], errors='coerce')
    df['MAX'] = pd.to_numeric(df['MAX'], errors='coerce')
    df['MIN'] = pd.to_numeric(df['MIN'], errors='coerce')
    df['PRCP'] = pd.to_numeric(df['PRCP'], errors='coerce')
    df['SNDP'] = pd.to_numeric(df['SNDP'], errors='coerce')

    with SessionLocal() as session:
        for _, row in df.iterrows():
            station_code = row['STATION']
            station = session.query(Station).filter(Station.station_code == station_code).first()
            if not station:
                station = Station(
                    station_code=row['STATION'],
                    name=row['NAME'],
                    latitude=row['LATITUDE'],
                    longitude=row['LONGITUDE'],
                    elevation=row['ELEVATION']
                )
                session.add(station)
                session.commit()
            
            year_obj = session.query(Year).filter(Year.year == year, Year.station_id == station.id).first()
            if not year_obj:
                year_obj = Year(year=year, station_id=station.id)
                session.add(year_obj)
                session.commit()

            weather_data = WeatherData(
                station_id=station.id,
                year_id=year_obj.id,
                date=row['DATE'],
                temp=row['TEMP'],
                dew_point=row['DEWP'],
                pressure=row['SLP'],
                visib=row['VISIB'],
                wind_speed=row['WDSP'],
                gust_speed=row['GUST'],
                max_temp=row['MAX'],
                min_temp=row['MIN'],
                precipitation=row['PRCP'],
                snow_depth=row['SNDP'],
                storm_flag=row['FRSHTT']
            )
            session.add(weather_data)
        session.commit()

for year in range(1997, 2003):
    fetch_and_process_data(year)
