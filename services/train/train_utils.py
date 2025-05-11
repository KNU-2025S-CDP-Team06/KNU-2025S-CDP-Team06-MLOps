import requests
from io import BytesIO
from config import config
import pandas as pd

def send_file(df : pd.DataFrame, category: str):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    files = {
        'revenue_file': (category+'_data.csv', csv_buffer, 'text/csv')
    }
    url = config.AI_TRIGGER_URL + '/train/'+category
    response = requests.post(url, files=files)

    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.text}")