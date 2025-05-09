import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta

from data_fetch import daily_data_fetcher, weather_fetcher, sales_fetcher
from repositories import store_repository, daily_data_repository, weather_repository, sales_repository

from utils.get_today import get_today

def add_daily_data_and_weather():
    target_date = get_today() - timedelta(days=1)
    stores = store_repository.get_all_stores()
    for store in stores:
        # 1. 일일 매출 데이터 저장
        daily_data = daily_data_fetcher.load_daily_data(store.mb_id, target_date)
        daily_data_repository.save_daily_data(store.mb_id, daily_data)

        # 2. 하루 모든 매출 데이터 저장
        sales_data = sales_fetcher.load_sales(store.mb_id, target_date)
        sales_repository.save_sales_data(store.mb_id, sales_data)

        # 3. 일일 날씨 데이터 저장
        weather_data = weather_fetcher.load_weather(store.latitude, store.longitude, target_date)
        weather_repository.save_weather(store.mb_id, weather_data)

if __name__ == '__main__':
    add_daily_data_and_weather()
    print(f"[Daily Task] {get_today() - timedelta(days=1)} 완료")