from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Station(Base):
    __tablename__ = 'stations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    elevation: Mapped[float] = mapped_column(Float)

    years = relationship('Year', back_populates='station')  
    weather_data = relationship('WeatherData', back_populates='station')


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey('stations.id'), nullable=False)
    year_id: Mapped[int] = mapped_column(Integer, ForeignKey('years.id'), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    temp: Mapped[float] = mapped_column(Float)
    dew_point: Mapped[float] = mapped_column(Float)
    pressure: Mapped[float] = mapped_column(Float)
    visib: Mapped[float] = mapped_column(Float)
    wind_speed: Mapped[float] = mapped_column(Float)
    gust_speed: Mapped[float] = mapped_column(Float)
    max_temp: Mapped[float] = mapped_column(Float)
    min_temp: Mapped[float] = mapped_column(Float)
    precipitation: Mapped[float] = mapped_column(Float)
    snow_depth: Mapped[float] = mapped_column(Float)
    storm_flag: Mapped[str] = mapped_column(String(10))

    station = relationship('Station', back_populates='weather_data')
    year = relationship('Year', back_populates='weather_data')


class Year(Base):
    __tablename__ = 'years'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey('stations.id'), nullable=False)

    station = relationship('Station', back_populates='years')  
    weather_data = relationship('WeatherData', back_populates='year')
