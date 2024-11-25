from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    station_code = Column(String, unique=True, nullable=False)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

    weather_data = relationship('WeatherData', back_populates='station')

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    date = Column(Date, nullable=False)
    temp = Column(Float)
    dew_point = Column(Float)
    pressure = Column(Float)
    visib = Column(Float)
    wind_speed = Column(Float)
    gust_speed = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precipitation = Column(Float)
    snow_depth = Column(Float)
    storm_flag = Column(String(10))

    station = relationship('Station', back_populates='weather_data')
