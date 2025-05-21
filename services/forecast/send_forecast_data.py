from . import forecast_utils

def send_forecast_data(period="daily"):
    forecast_utils.integration(period)