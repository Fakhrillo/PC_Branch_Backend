from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .views.camera_status import update_camera_statuses

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_camera_statuses, 'interval', seconds=600)
    scheduler.start()