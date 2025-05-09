from datetime import datetime

def get_today():
    now = datetime.now()
    today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return today_midnight