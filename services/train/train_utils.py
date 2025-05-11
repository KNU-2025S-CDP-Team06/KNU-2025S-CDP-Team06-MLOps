import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import requests
from sqlalchemy.orm import Session
from database.db_manager import SessionLocal
from io import BytesIO
from config import config
import pandas as pd
from database.models import DailyData, Store, Weather

def send_file(df : pd.DataFrame, category: str):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    files = {
        'train_file': (category+'_data.csv', csv_buffer, 'text/csv')
    }
    url = config.AI_TRIGGER_URL + '/train/'+category
    response = requests.post(url, files=files)

    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.text}")

def load_data(category : str):

    session: Session = SessionLocal()

    if category == 'cluster':
        results = session.query(
            DailyData.store_id,
            DailyData.date,
            DailyData.total_revenue
        ).all()
        
        if not results:
            print("보낼 매출 데이터가 없습니다.")
            return

        return pd.DataFrame([{
            "store_id": row.store_id,
            "date": row.date,
            "revenue": row.total_revenue,
        } for row in results])

    elif category == 'prophet':
        results = session.query(
            DailyData.store_id,
            Store.cluster,
            DailyData.date,
            DailyData.total_revenue
        ).join(Store, DailyData.store_id == Store.id).all()

        if not results:
            print("보낼 매출 데이터가 없습니다.")
            return

        return pd.DataFrame([{
            "store_id": row.store_id,
            "cluster_id": row.cluster,
            "date": row.date,
            "revenue": row.total_revenue,
        } for row in results])
    
    elif category == 'xgboost':
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

        return pd.DataFrame([{
            "store_id": row.store_id,
            "cluster_id": row.cluster,
            "date": row.date,
            "revenue": row.total_revenue,
            "rain": row.precipitation,
            "weather": row.weather,
            "temp": row.feeling,
        } for row in results])
    
def integration(category: str):
    try:
        df = load_data(category)
        send_file(df, category)
    except Exception as e:
        print(f"클러스터 데이터 전송 오류: {e}")