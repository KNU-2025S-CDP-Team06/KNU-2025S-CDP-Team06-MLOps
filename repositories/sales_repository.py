import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import Sales, Store, Menu, DailyData
from sqlalchemy import func

def save_sales_data(mb_id, sales_data_list):
    """매출 데이터 저장 (중복된 id가 있으면 업데이트)"""
    session = SessionLocal()
    try:
        if sales_data_list:
            for sales_data in sales_data_list:
                # 1. mb_id로 store_id 찾기, date와 store_id로 daily_data 찾기
                store = session.query(Store).filter(Store.mb_id == mb_id).first()
                daily_data = (session.query(DailyData).filter(func.date(DailyData.date) == sales_data["datetime"].date(), DailyData.store_id == store.id).first())

                if not store:
                    print(f"매장 정보 없음: {mb_id}")
                    return
                if not daily_data:
                    print(f"일일 매출 정보 없음: {sales_data.datetime}")
                    return

                sales_data["store_id"] = store.id  # store_id 매핑
                sales_data['daily_data_id'] = daily_data.id # daliy_data_id 매핑
                sales_data.pop('mb_id', None) # mb_id 삭제

                # 2. 기존 매출 데이터 확인
                exsiting_sales_data = session.query(Sales).filter(
                    (Sales.store_id == sales_data["store_id"]) & 
                    (Sales.datetime == sales_data["datetime"]) &
                    (Sales.daily_data_id == sales_data["daily_data_id"])
                ).first()
                
                if exsiting_sales_data:
                    # 기존 데이터 업데이트
                    for key, value in sales_data.items():
                        setattr(exsiting_sales_data, key, value)
                else:
                    # 새로운 데이터 삽입
                    new_sales_data = Sales(**sales_data)
                    session.add(new_sales_data)
                    print(f"1회 판매 데이터 저장 완료: sales_datetime={sales_data['datetime']}")
                session.commit()
    except Exception as e:
        session.rollback()
        print(f"sales 저장/업데이트 오류: {e}")
    finally:
        session.close()

# def get_sales_data_by_date(date):
#     """특정 날짜의 매출 데이터 조회"""
#     session = SessionLocal()
#     try:
#         return session.query(Sales).filter(func.date(Sales.datetime) == date.date()).all()
#     finally:
#         session.close()

# def get_sales_data_by_store(store_id):
#     """특정 매장의 매출 데이터 조회"""
#     session = SessionLocal()
#     try:
#         return session.query(Sales).filter(Sales.store_id == store_id).all()
#     finally:
#         session.close()

# def delete_daily_data_by_date(date):
#     """특정 날짜의 매출 데이터 삭제"""
#     session = SessionLocal()
#     try:
#         session.query(Sales).filter(Sales.datetime == date).delete()
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         print(f"매출 삭제 오류: {e}")
#     finally:
#         session.close()