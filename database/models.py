from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship,declarative_base

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))

Base = declarative_base()

class Store(Base):
    __tablename__ = "store" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    mb_id = Column(String(50), nullable=False, unique=True)  # 사업자 번호
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=True)

    # 관계 설정 (1:N)
    sales = relationship("Sales", backref="store", cascade="all, delete")
    weather = relationship("Weather", backref="store", cascade="all, delete")

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    date = Column(DateTime, nullable=False)  # 매출 발생 날짜
    revenue = Column(Float, nullable=False)  # 매출 금액

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('store.id', ondelete="CASCADE"), nullable=False)  # FK (매장 ID)
    date = Column(DateTime, nullable=False)  # 날씨 기록 날짜
    weekday = Column(Integer, nullable=False) # 날씨 기록 요일
    feeling = Column(Float, nullable=False)  # 체감 기온
    precipitation = Column(Float, nullable=True)  # 강수량
    weather = Column(String(255), nullable=False) # 날씨
