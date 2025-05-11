import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
import requests
from io import BytesIO
from sqlalchemy.orm import Session
from database.db_manager import SessionLocal
from database.models import DailyData
from config import config

def send_cluster_data():
    session: Session = SessionLocal()
    try:
        results = session.query(
            DailyData.store_id,
            DailyData.date,
            DailyData.total_revenue
        ).all()

        if not results:
            print("보낼 매출 데이터가 없습니다.")
            return

        df = pd.DataFrame([{
            "store_id": row.store_id,
            "date": row.date,
            "revenue": row.total_revenue,
        } for row in results])

        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        files = {
            'revenue_file': ('sales_data.csv', csv_buffer, 'text/csv')
        }
        url = config.AI_TRIGGER_URL + '/train/cluster'
        response = requests.post(url, files=files)

        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.text}")

    except Exception as e:
        print(f"클러스터 데이터 전송 오류: {e}")
    finally:
        session.close()
        