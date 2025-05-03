import sys
import os
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

def load_daily_data(mb_id: str, current_date:datetime):
    date = current_date.strftime("%Y-%m-%d")
    params = {
        "mb_id" : mb_id,
        "date" : date
    }
    url = config.MOKI_SALES_API_URL
    daily_data = requests.get(url, params=params).json()

    daily_revenue = daily_data["total_revenue"]
    daily_count = daily_data["total_count"]
    daily_data_info = {
        "date" : date,
        "total_revenue" : daily_revenue,
        "total_count": daily_count
    }

    return daily_data_info