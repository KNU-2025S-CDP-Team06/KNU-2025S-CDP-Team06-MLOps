from apscheduler.schedulers.blocking import BlockingScheduler
from daily_tasks import add_sales_and_weather

scheduler = BlockingScheduler()

# 매일 자정 (00:00)에 실행
@scheduler.scheduled_job('cron', hour=0, minute=0)
def scheduled_task():
    add_sales_and_weather()

if __name__ == "__main__":
    scheduler.start()