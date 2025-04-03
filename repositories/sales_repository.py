import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import Sales, Store
from sqlalchemy import func

def save_sales(mb_id, sales_data):
    """매출 데이터 저장 (중복된 id가 있으면 업데이트)"""
    session = SessionLocal()
    try:
        # 1. mb_id로 store_id 찾기
        store = session.query(Store).filter(Store.mb_id == mb_id).first()
        if not store:
            print(f"매장 정보 없음: {mb_id}")
            return

        sales_data["store_id"] = store.id  # store_id 매핑

        # 2. 기존 매출 데이터 확인
        sales = session.query(Sales).filter(
            (Sales.store_id == sales_data["store_id"]) & 
            (Sales.date == sales_data["date"])
        ).first()
        
        if sales:
            # 기존 데이터 업데이트
            for key, value in sales_data.items():
                setattr(sales, key, value)
        else:
            # 새로운 데이터 삽입
            sales = Sales(**sales_data)
            session.add(sales)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"매출 저장/업데이트 오류: {e}")
    finally:
        session.close()

def get_sales_by_date(date):
    """특정 날짜의 매출 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(Sales).filter(func.date(Sales.date) == date.date()).all()
    finally:
        session.close()

def get_sales_by_store(store_id):
    """특정 매장의 매출 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(Sales).filter(Sales.store_id == store_id).all()
    finally:
        session.close()

def delete_sales_by_date(date):
    """특정 날짜의 매출 데이터 삭제"""
    session = SessionLocal()
    try:
        session.query(Sales).filter(Sales.date == date).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"매출 삭제 오류: {e}")
    finally:
        session.close()