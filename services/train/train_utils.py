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

def send_file(df1, category, df2=None):
    buffer1 = BytesIO()
    df1.to_csv(buffer1, index=False)
    buffer1.seek(0)

    files = [
        ('train_file', (f'{category}_data_1.csv', buffer1, 'text/csv'))
    ]

    if df2 is not None:
        buffer2 = BytesIO()
        df2.to_csv(buffer2, index=False)
        buffer2.seek(0)
        files.append(('train_file', (f'{category}_data_2.csv', buffer2, 'text/csv')))

    url = config.AI_TRIGGER_URL + f'/train/{category}'
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

        return [pd.DataFrame(results, columns=["store_id", "date", "revenue"])]

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

        return [pd.DataFrame(results, columns=["store_id", "cluster_id", "date", "revenue"])]
    
    elif category == 'xgboost':

        sales_results = session.query(
            DailyData.store_id,
            Store.cluster,
            DailyData.date,
            DailyData.total_revenue
        ).join(Store, DailyData.store_id == Store.id).all()

        weather_results = session.query(
            Weather.store_id,
            Store.cluster,
            Weather.date,
            Weather.precipitation,
            Weather.weather,
            Weather.feeling
        ).join(Store, Weather.store_id == Store.id
        ).all()

        if (not sales_results) or (not weather_results):
            print("보낼 데이터가 없습니다.")
            return

        sales_df = pd.DataFrame(sales_results, columns=[
            'store_id', 'cluster', 'date', 'total_revenue'
        ])

        weather_df = pd.DataFrame(weather_results, columns=[
            'store_id', 'cluster', 'date', 'precipitation', 'weather', 'feeling'
        ])

        return [sales_df, weather_df]
    
def integration(category: str):
    try:
        df_list = load_data(category)
        if len(df_list) == 1:
            send_file(df_list[0], category)
        elif len(df_list) == 2:
            send_file(df_list[0], category, df_list[1])
    except Exception as e:
        print(f"클러스터 데이터 전송 오류: {e}")