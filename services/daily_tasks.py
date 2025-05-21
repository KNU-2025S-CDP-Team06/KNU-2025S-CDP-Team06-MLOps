import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta

from data_fetch import daily_data_fetcher, weather_fetcher, sales_fetcher
from repositories import store_repository, daily_data_repository, weather_repository, sales_repository

from utils.get_today import get_today
from forecast.send_forecast_data import send_forecast_data

def daily_tasks():
    target_date = get_today() - timedelta(days=1)
    forecast_date = get_today() + timedelta(days=1)
    stores = store_repository.get_all_stores()
    for store in stores:
        # 1. 일일 매출 데이터 저장
        daily_data = daily_data_fetcher.load_daily_data(store.mb_id, target_date)
        daily_data_repository.save_daily_data(store.mb_id, daily_data)

        # 2. 하루 모든 매출 데이터 저장
        sales_data = sales_fetcher.load_sales(store.mb_id, target_date)
        sales_repository.save_sales_data(store.mb_id, sales_data)

        # 3. 일일 날씨 데이터 저장
        weather_data = weather_fetcher.load_history_weather(store.latitude, store.longitude, target_date)
        weather_repository.save_weather(store.mb_id, weather_data)

        # 4. 내일 날씨 데이터 저장
        forecast_weather_data = weather_fetcher.load_forecast_weather(store.latitude, store.longitude, forecast_date)
        weather_repository.save_weather(store.mb_id, forecast_weather_data)

    # 5. 내일 날시 데이터 및 과거 매출 데이터 기반으로 예측값 요청 후 DB에 저장
    from datetime import datetime, timedelta
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    if tomorrow.day == 1:
        send_forecast_data("monthly") # 매월 말일 데이터 전송
    elif today.weekday() == 6:
        send_forecast_data("weekly") # 매주 일요일 데이터 전송
    else:
        send_forecast_data() # 매일 데이터 전송

if __name__ == '__main__':
    daily_tasks()
    print(f"[Daily Task] {datetime.now()} 완료")