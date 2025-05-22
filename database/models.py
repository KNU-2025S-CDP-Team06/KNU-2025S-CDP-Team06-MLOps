from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship,declarative_base
import enum

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))

Base = declarative_base()
class Role(enum.Enum):
    STORE = "STORE"
    ADMIN = "ADMIN"

class Store(Base):
    __tablename__ = "store" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    mb_id = Column(String(50), nullable=False, unique=True)  # 사업자 번호
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    cluster = Column(Integer, nullable=True)
    password = Column(String, nullable=False)

    role = Column(Enum(Role), default=Role.STORE, nullable=True)

    # 관계 설정 (1:N)
    dailyData = relationship("DailyData", backref="store", cascade="all, delete")
    forecast = relationship("Forecast", backref="store", cascade="all, delete")
    weather = relationship("Weather", backref="store", cascade="all, delete")

class DailyData(Base):
    __tablename__ = "daily_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    date = Column(DateTime, nullable=False)  # 매출 발생 날짜
    total_revenue = Column(Integer, nullable=True)  # 총 매출 금액
    total_count = Column(Integer, nullable=True)  # 총 판매 개수

    # 관계 설정 (1:N)
    sales = relationship("Sales", backref="daily_data", cascade="all, delete")

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_data_id = Column(Integer, ForeignKey('daily_data.id', ondelete="CASCADE"), nullable=False) # FK (DaliyData ID)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete="CASCADE"), nullable=False)  # FK (메뉴 ID)
    datetime = Column(DateTime, nullable=False)  # 판매 시간
    count = Column(Integer, nullable=False)  # 판매 개수

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False) # 메뉴명
    image = Column(String(255), nullable=True) # 메뉴 이미지 URL
    price = Column(Integer, nullable=True) # 메뉴 가격

    # 관계 설정 (1:N)
    sales = relationship("Sales", backref="menu", cascade="all, delete")

class Forecast(Base):
    __tablename__ = "forecast"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    date = Column(DateTime, nullable=False)  # 예측 날짜
    prophet_forecast = Column(Integer, nullable=False) # Prophet 모델 예측 매출액
    xgboost_forecast = Column(Float, nullable=True) # XGBoost 모델 예측 증감률
    

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    date = Column(DateTime, nullable=False)  # 날씨 기록 날짜
    weekday = Column(Integer, nullable=False) # 날씨 기록 요일
    feeling = Column(Float, nullable=False)  # 체감 기온
    precipitation = Column(Float, nullable=True)  # 강수량
    weather = Column(String(255), nullable=False) # 날씨
