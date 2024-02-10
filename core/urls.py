from django.urls import path
from .views.camera_d import CameraDetailsAPI, CameraDetailsWithData, CameraWith24HoursData
from .views.checkouts import CheckoutsAPI, CheckoutUpdateAPI, CheckoutDeleteAPI
from .views.notifications import NotificationsAPI
from .views.workers import WorkersAPI, GET_TOKEN, WorkerUpdateAPI, WorkerDeleteAPI, IsWorkerExist

urlpatterns = [
    path('camera_details/', CameraDetailsAPI.as_view()),
    path('camera_details_with_data/', CameraDetailsWithData.as_view()),
    path('camera_diagram_with_data/', CameraWith24HoursData.as_view()),

    path('checkouts/', CheckoutsAPI.as_view()),
    path('checkouts_update/', CheckoutUpdateAPI.as_view()),
    path('checkouts_delete/', CheckoutDeleteAPI.as_view()),

    path('notifications/', NotificationsAPI.as_view()),
    path('workers/', WorkersAPI.as_view()),
    path('check_worker/', IsWorkerExist.as_view()),
    path('workers_update/', WorkerUpdateAPI.as_view()),
    path('workers_delete/', WorkerDeleteAPI.as_view()),

    path("get_token/", GET_TOKEN.as_view()),
]
