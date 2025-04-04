import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta

from data_fetch import sales_fetcher, weather_fetcher
from repositories import store_repository, sales_repository, weather_repository

def add_sales_and_weather():
    target_date = datetime.today() - timedelta(days=1)
    stores = store_repository.get_all_stores()

    for store in stores:
        sales_data = sales_fetcher.load_sales(store.mb_id, target_date)
        sales_repository.save_sales(store.mb_id, sales_data)

        weather_data = weather_fetcher.load_weather(store.latitude, store.longitude, target_date)
        weather_repository.save_weather(store.mb_id, weather_data)

    print(f"{target_date.strftime('%Y-%m-%d')} 매출 및 날씨 데이터 업데이트 완료")
    