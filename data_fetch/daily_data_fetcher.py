import sys
import os
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

def load_sales(mb_id: str, current_date:datetime):
    date = current_date.strftime("%Y-%m-%d")
    params = {
        "mb_id" : mb_id,
        "date" : date
    }
    url = config.MOKI_SALES_API_URL
    sales_data = requests.get(url, params=params).json()

    daily_revenue = sales_data["total_revenue"]
    sales_info = {
        "date" : date,
        "revenue" : daily_revenue
    }

    return sales_info