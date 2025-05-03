import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_manager import SessionLocal
from database.models import Menu

def save_menu_data(menu_data_list):
    """매출 데이터 저장 (중복된 id가 있으면 업데이트)"""
    session = SessionLocal()
    try:
        for menu_data in menu_data_list:
            # key 값 변경
            menu_data["id"] = menu_data.pop("menu_id")
            menu_data["name"] = menu_data.pop("menu_name")
            menu_data["image"] = menu_data.pop("menu_img")

            # 1. 기존 메뉴 데이터 확인
            exsiting_menu_data = session.query(Menu).filter((Menu.id == menu_data["id"])).first()
            
            if exsiting_menu_data:
                # 기존 데이터 업데이트
                for key, value in menu_data.items():
                    setattr(exsiting_menu_data, key, value)
            else:
                # 새로운 데이터 삽입
                new_menu_data = Menu(**menu_data)
                session.add(new_menu_data)

            session.commit()
    except Exception as e:
        session.rollback()
        print(f"menu 저장/업데이트 오류: {e}")
    finally:
        session.close()