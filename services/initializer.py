import sys, os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from daily_tasks import daily_tasks

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.get_today import get_today
from data_fetch import (
    daily_data_fetcher,
    store_fetcher,
    weather_fetcher,
    menu_fetcher,
    sales_fetcher,
)
from repositories import (
    store_repository,
    daily_data_repository,
    weather_repository,
    menu_repository,
    sales_repository,
)

MAX_WORKERS = 15  # 병렬 스레드 수 (네트워크/서버 상황 따라 조절)

def initialize_store_data():
    stores = store_fetcher.load_store_data()
    for store_name in stores:
        store_data = store_fetcher.fetch_store(stores[store_name], store_name)
        store_repository.save_store(store_data)

def initialize_menu_data():
    stores = store_fetcher.load_store_data()
    for store_name in stores:
        menu_data = menu_fetcher.load_menu(stores[store_name])
        menu_repository.save_menu_data(menu_data)

def fetch_weather_for_date(mb_id, lat, lng, current_date):
    weather_data = weather_fetcher.load_history_weather(lat, lng, current_date)
    weather_repository.save_weather(mb_id, weather_data)

def initialize_weather_data_parallel():
    stores = store_fetcher.load_store_data()
    end_date = get_today() - timedelta(days=2)
    start_date = end_date - timedelta(days=364)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for store_name, mb_id in stores.items():
            store_data = store_repository.get_store_by_mb_id(mb_id)
            lat, lng = store_data.latitude, store_data.longitude
            current_date = start_date
            while current_date <= end_date:
                futures.append(
                    executor.submit(fetch_weather_for_date, mb_id, lat, lng, current_date)
                )
                current_date += timedelta(days=1)

        for future in as_completed(futures):
            future.result()

def fetch_daily_for_date(mb_id, current_date):
    daily_data = daily_data_fetcher.load_daily_data(mb_id, current_date)
    daily_data_repository.save_daily_data(mb_id, daily_data)

def initialize_daily_data_parallel():
    stores = store_fetcher.load_store_data()
    end_date = get_today() - timedelta(days=2)
    start_date = end_date - timedelta(days=729)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for store_name, mb_id in stores.items():
            current_date = start_date
            while current_date <= end_date:
                futures.append(
                    executor.submit(fetch_daily_for_date, mb_id, current_date)
                )
                current_date += timedelta(days=1)

        for future in as_completed(futures):
            future.result()

def fetch_sales_for_date(mb_id, current_date):
    sales_data = sales_fetcher.load_sales(mb_id, current_date)
    sales_repository.save_sales_data(mb_id, sales_data)


def initialize_sales_data_parallel_store_date():
    stores = store_fetcher.load_store_data()
    end_date = get_today() - timedelta(days=2)
    start_date = end_date - timedelta(days=729)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for store_name, mb_id in stores.items():
            current_date = start_date
            while current_date <= end_date:
                futures.append(
                    executor.submit(fetch_sales_for_date, mb_id, current_date)
                )
                current_date += timedelta(days=1)

        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    print(f"[Initializer] {datetime.now()} Store Data 시작")
    initialize_store_data()

    print(f"[Initializer] {datetime.now()} Menu Data 시작")
    initialize_menu_data()

    print(f"[Initializer] {datetime.now()} Weather & Daily Data 시작")
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_weather = executor.submit(initialize_weather_data_parallel)
        future_daily = executor.submit(initialize_daily_data_parallel)
        future_weather.result()
        future_daily.result()

    print(f"[Initializer] {datetime.now()} Sales Data 시작")
    initialize_sales_data_parallel_store_date()

    print(f"[Initializer] {datetime.now()} 완료")
    
    daily_tasks()
    print(f"[Daily Task] {datetime.now()} 완료")