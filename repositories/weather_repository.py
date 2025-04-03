import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import Store, Weather
from sqlalchemy import func

def save_weather(mb_id, weather_data):
    """날씨 데이터 저장 (store_id 매핑 후 저장)"""
    session = SessionLocal()
    try:
        # 1. mb_id로 store_id 찾기
        store = session.query(Store).filter(Store.mb_id == mb_id).first()
        if not store:
            print(f"매장 정보 없음: {mb_id}")
            return

        weather_data["store_id"] = store.id  # store_id 매핑

        # 2. 기존 날씨 데이터 확인
        weather = session.query(Weather).filter(
            (Weather.store_id == weather_data["store_id"]) & 
            (Weather.date == weather_data["date"])
        ).first()

        if weather:
            # 기존 데이터 업데이트
            for key, value in weather_data.items():
                setattr(weather, key, value)
        else:
            # 새로운 데이터 삽입
            weather = Weather(**weather_data)
            session.add(weather)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"날씨 저장/업데이트 오류: {e}")
    finally:
        session.close()

def get_weather_by_date(date):
    """특정 날짜의 날씨 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(Weather).filter(func.date(Weather.date) == date.date()).all()
    finally:
        session.close()

def get_weather_by_store(store_id):
    """특정 매장의 날씨 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(Weather).filter(Weather.store_id == store_id).all()
    finally:
        session.close()

def delete_weather_by_date(date):
    """특정 날짜의 날씨 데이터 삭제"""
    session = SessionLocal()
    try:
        session.query(Weather).filter(Weather.date == date).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"날씨 삭제 오류: {e}")
    finally:
        session.close()