import requests
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Camera_details

def update_camera_statuses():
    cameras = Camera_details.objects.all()

    for camera in cameras:
        try:
            response = requests.get(f'http://91.196.77.156:8005/camera/last_data/?Cam_MxID={camera.MxID}')
            data = response.json()

            # Parse the datetime string from the response
            last_data_time = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

            # Check if the last data is within the last 10 minutes
            if timezone.now() - last_data_time <= timedelta(minutes=10):
                camera.status = True
            else:
                camera.status = False

            camera.save()

        except Exception as e:
            print(f"Error updating status for camera {camera.MxID}: {e}")

