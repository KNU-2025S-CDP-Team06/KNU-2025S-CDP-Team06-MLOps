import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import DailyData, Store
from sqlalchemy import func

def save_daily_data(mb_id, daily_data):
    """매출 데이터 저장 (중복된 id가 있으면 업데이트)"""
    session = SessionLocal()
    try:
        # 1. mb_id로 store_id 찾기
        store = session.query(Store).filter(Store.mb_id == mb_id).first()
        if not store:
            print(f"매장 정보 없음: {mb_id}")
            return

        daily_data["store_id"] = store.id  # store_id 매핑

        # 2. 기존 매출 데이터 확인
        exsiting_daily_data = session.query(DailyData).filter(
            (DailyData.store_id == daily_data["store_id"]) & 
            (DailyData.date == daily_data["date"])
        ).first()
        
        if exsiting_daily_data:
            # 기존 데이터 업데이트
            for key, value in daily_data.items():
                setattr(exsiting_daily_data, key, value)
        else:
            # 새로운 데이터 삽입
            new_daily_data = DailyData(**daily_data)
            session.add(new_daily_data)
            print(f"일일 판매 데이터 저장 완료: daily_data_date={daily_data['date']}")
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"매출 저장/업데이트 오류: {e}")
    finally:
        session.close()

def get_daily_data_by_date(date):
    """특정 날짜의 매출 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(DailyData).filter(func.date(DailyData.date) == date.date()).all()
    finally:
        session.close()

def get_daily_data_by_store(store_id):
    """특정 매장의 매출 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(DailyData).filter(DailyData.store_id == store_id).all()
    finally:
        session.close()

def delete_daily_data_by_date(date):
    """특정 날짜의 매출 데이터 삭제"""
    session = SessionLocal()
    try:
        session.query(DailyData).filter(DailyData.date == date).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"매출 삭제 오류: {e}")
    finally:
        session.close()