import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import Store

def save_store(store_data):
    """매장 데이터 저장 (중복된 id가 있으면 업데이트)"""
    session = SessionLocal()
    try:
        store = session.query(Store).filter(Store.mb_id == store_data["mb_id"]).first()
        if store:
            # 기존 데이터 업데이트
            for key, value in store_data.items():
                setattr(store, key, value)
        else:
            # 새로운 데이터 삽입
            store = Store(**store_data)
            session.add(store)

        print(f"매장 저장 완료: mb_id={store.mb_id}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"매장 저장/업데이트 오류: {e}")
    finally:
        session.close()

def get_all_stores():
    """모든 매장 데이터 조회"""
    session = SessionLocal()
    try:
        return session.query(Store).all()
    finally:
        session.close()

def get_store_by_mb_id(mb_id):
    """사업자 ID로 조회"""
    session = SessionLocal()
    try:
        return session.query(Store).filter(Store.mb_id == mb_id).first()
    finally:
        session.close()

def delete_store(store_id):
    """매장 데이터 삭제"""
    session = SessionLocal()
    try:
        store = session.query(Store).filter(Store.store_id == store_id).first()
        if store:
            session.delete(store)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"매장 삭제 오류: {e}")
    finally:
        session.close()