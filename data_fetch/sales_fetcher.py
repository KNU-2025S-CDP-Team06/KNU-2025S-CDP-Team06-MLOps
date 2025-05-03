import sys
import os
import requests
from datetime import datetime
from pprint import pprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

def load_sales(mb_id: str, current_date:datetime):
    date = current_date.strftime("%Y-%m-%d")
    params = {
        "mb_id" : mb_id,
        "date" : date
    }
    url = config.MOKI_SALES_API_URL
    sales_data_list = requests.get(url, params=params).json()['data']
    
    if sales_data_list:
        sales_info = []
        for sales_data in sales_data_list:
            date_time_str = f"{sales_data['date']} {sales_data['hour']}:00:00"
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            sales_info.append( {
                "mb_id" : mb_id,
                "menu_id" : sales_data['menu_id'],
                "count" : sales_data['count'],
                "datetime" : date_time_obj
            })
        return sales_info