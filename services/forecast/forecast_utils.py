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
from datetime import date, timedelta
from pprint import pprint

def load_data():
    session: Session = SessionLocal()

    today = date.today() - timedelta(days=5)
    target_dates = [
        today - timedelta(days=1),
        today - timedelta(days=2),
        today - timedelta(days=7),
        today - timedelta(days=14),
    ]

    # 오늘 기준 base 데이터
    base_results = (
        session.query(
            DailyData.store_id,
            Store.cluster,
            DailyData.date,
            Weather.precipitation,
            Weather.weather,
            Weather.feeling
        )
        .join(Store, DailyData.store_id == Store.id)
        .outerjoin(
            Weather,
            (DailyData.store_id == Weather.store_id) &
            (DailyData.date == Weather.date)
        )
        .filter(DailyData.date == today)
        .all()
    )

    if not base_results:
        print("오늘 날짜의 매출 데이터가 없습니다.")
        return

    # 과거 매출 데이터 가져오기
    past_results = (
        session.query(
            DailyData.store_id,
            DailyData.date,
            DailyData.total_revenue
        )
        .filter(DailyData.date.in_(target_dates))
        .all()
    )

    # base_df 구성
    base_df = pd.DataFrame([{
        "store_id": row.store_id,
        "cluster_id": row.cluster,
        "date": row.date,
        "precipitation": row.precipitation,
        "weather": row.weather,
        "feeling": row.feeling
    } for row in base_results])

    # 과거 매출 df 구성
    past_df = pd.DataFrame([{
        "store_id": row.store_id,
        "date": row.date,
        "revenue": row.total_revenue
    } for row in past_results])

    pprint(past_df)

    # 각 날짜 기준 revenue 붙이기
    base_df["key"] = base_df["store_id"].astype(str) + "_" + base_df["date"].astype(str)

    for d in [1, 2, 7, 14]:
        dt_col = base_df["date"] - timedelta(days=d)
        base_df[f"merge_key_t-{d}"] = base_df["store_id"].astype(str) + "_" + dt_col.astype(str)

        temp_df = past_df.copy()
        temp_df["key"] = temp_df["store_id"].astype(str) + "_" + temp_df["date"].astype(str)
        temp_df = temp_df[["key", "revenue"]].rename(columns={"revenue": f"rev_t-{d}"})

        base_df = base_df.merge(temp_df, left_on=f"merge_key_t-{d}", right_on="key", how="left")
        base_df.drop(columns=["key"], inplace=True, errors="ignore")

    # key와 merge_key로 시작하는 컬럼 삭제
    base_df.drop(columns=[col for col in base_df.columns if col.startswith("key") or col.startswith("merge_key")], inplace=True)

    return base_df

def send_file(df : pd.DataFrame):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    files = {
        'forecast_file': ('forecast_data.csv', csv_buffer, 'text/csv')
    }
    url = config.AI_TRIGGER_URL + '/forecast/daily'
    response = requests.post(url, files=files)

    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.text}")

def integration():
    try:
        send_file(load_data())
    except Exception as e:
        print(f"클러스터 데이터 전송 오류: {e}")
