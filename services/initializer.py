import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta

from data_fetch import store_fetcher, sales_fetcher, weather_fetcher
from repositories import store_repository, sales_repository, weather_repository

def initialize_store_data():
    stores = store_fetcher.load_store_data()
    for store_name in stores:
        store_data = store_fetcher.fetch_store(stores[store_name],store_name)
        store_repository.save_store(store_data)

def initialize_sales_data():
    stores = store_fetcher.load_store_data()
    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=365 * 2) # 2년

    for store_name in stores:
        current_date = start_date
        mb_id = stores[store_name]
        while current_date <= end_date:
            sales_data = sales_fetcher.load_sales(mb_id, current_date)
            sales_repository.save_sales(mb_id, sales_data)
            current_date += timedelta(days=1)

def initialize_weather_data():
    stores = store_fetcher.load_store_data()
    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=365) # 1년

    for store_name in stores:
        current_date = start_date
        mb_id = stores[store_name]
        store_data = store_repository.get_store_by_mb_id(mb_id)
        lat, lng = store_data.latitude, store_data.longitude
        while current_date <= end_date:
            weather_data = weather_fetcher.load_weather(lat, lng, current_date)
            weather_repository.save_weather(mb_id, weather_data)
            weather_list = weather_repository.get_weather_by_date(current_date)
            for weather in weather_list:
                print(weather.__dict__)
            current_date += timedelta(days=1)

if __name__ == '__main__':
    initialize_store_data()
    initialize_weather_data()
    # initialize_sales_data()
    print(f"[Initializer] {datetime.now()} 완료")