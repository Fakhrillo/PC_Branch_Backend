from django.urls import path
from .views.camera_d import CameraDetailsAPI, CameraDetailsWithData, CameraWith24HoursData
from .views.checkouts import CheckoutsAPI
from .views.notifications import NotificationsAPI
from .views.workers import WorkersAPI

urlpatterns = [
    path('camera_details/', CameraDetailsAPI.as_view()),
    path('camera_details_with_data/', CameraDetailsWithData.as_view()),
    path('camera_diagram_with_data/', CameraWith24HoursData.as_view()),

    path('checkouts/', CheckoutsAPI.as_view()),
    path('notifications/', NotificationsAPI.as_view()),
    path('workers/', WorkersAPI.as_view()),
]
