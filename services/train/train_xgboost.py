import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from sqlalchemy.orm import Session
from database.db_manager import SessionLocal
from database.models import DailyData, Store, Weather
import train_utils

def send_xgboost_data():
    session: Session = SessionLocal()
    try:
        results = session.query(
            DailyData.store_id,
            Store.cluster,
            DailyData.date,
            DailyData.total_revenue,
            Weather.precipitation,
            Weather.weather,
            Weather.feeling
        ).join(Store, DailyData.store_id == Store.id
        ).join(Weather, (DailyData.store_id == Weather.store_id) & (DailyData.date == Weather.date)
        ).all()

        if not results:
            print("보낼 매출 데이터가 없습니다.")
            return

        df = pd.DataFrame([{
            "store_id": row.store_id,
            "cluster_id": row.cluster,
            "date": row.date,
            "revenue": row.total_revenue,
            "rain": row.precipitation,
            "weather": row.weather,
            "temp": row.feeling,
        } for row in results])

        train_utils.send_file(df, 'xgboost')

    except Exception as e:
        print(f"클러스터 데이터 전송 오류: {e}")
    finally:
        session.close()
