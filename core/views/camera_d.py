from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser
import requests
from collections import defaultdict
from datetime import datetime
from environs import Env
env = Env()
env.read_env()

from ..models import *
from ..serializers import CameraDSerializer

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        print(request.user)
        return bool(request.user and request.user.is_superuser)

class CameraDetailsAPI(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    authentication_classes = [JWTAuthentication]

    queryset = Camera_details.objects.all()
    serializer_class = CameraDSerializer

class CameraDetailsWithData(APIView):
    permission_classes = [IsAdminUser, IsSuperUser]
    authentication_classes = [JWTAuthentication]

    jwt_access_token = None

    def get(self, request, *args, **kwargs):
        global jwt_access_token

        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        camera_objects = Camera_details.objects.all()
        combined_details = defaultdict(lambda: {"incoming": 0, "outgoing": 0})

        username = env("USERNAME")
        password = env("PASSWORD")
        API_URL = env("API_URL")
        
        get_token(username, password)
        headers = {'Authorization': f'Bearer {jwt_access_token}'}

        for camera_object in camera_objects:
            cam_mxid = camera_object.MxID
            url = f"{API_URL}camera/tracked/{cam_mxid}"

            if start_date_str and end_date_str:
                url += f"?start_date={start_date_str}&end_date={end_date_str}"

            response = requests.get(url, headers=headers) 

            if response.status_code == 200:
                count_details = response.json()

                for entry in count_details:
                    combined_details[cam_mxid]["incoming"] += entry["incoming"]
                    combined_details[cam_mxid]["outgoing"] += entry["outgoing"]

        response_data = []

        for cam_mxid, details in combined_details.items():
            response_data.append({
                "MxID": cam_mxid,
                "details": {
                    "located": camera_objects.filter(MxID=cam_mxid).first().located,
                    "status": camera_objects.filter(MxID=cam_mxid).first().status,
                    "stream_link": camera_objects.filter(MxID=cam_mxid).first().stream_link,
                    "created_at": camera_objects.filter(MxID=cam_mxid).first().created_at,
                },
                "data": {
                    "incoming": details["incoming"],
                    "outgoing": details["outgoing"],
                    "start_date": start_date_str if start_date_str else "N/A",
                    "end_date": end_date_str if end_date_str else "N/A",
                }
            })

        return Response(response_data)


class CameraWith24HoursData(APIView):
    permission_classes = [IsAdminUser, IsSuperUser]
    authentication_classes = [JWTAuthentication]

    jwt_access_token = None

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        camera_objects = Camera_details.objects.all()
        combined_details = defaultdict(lambda: {"data": {}})

        username = env("USERNAME")
        password = env("PASSWORD")
        API_URL = env("API_URL")
        
        get_token(username, password)
        headers = {'Authorization': f'Bearer {jwt_access_token}'}

        for camera_object in camera_objects:
            cam_mxid = camera_object.MxID
            url = f"{API_URL}camera/tracked/{cam_mxid}"

            if start_date_str and end_date_str:
                url += f"?start_date={start_date_str}&end_date={end_date_str}"

            response = requests.get(url, headers=headers) 

            if response.status_code == 200:
                count_details = response.json()

                for entry in count_details:
                    created_at = datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    hour = created_at.strftime("%H")
                    date = created_at.strftime("%Y-%m-%d")

                    if date not in combined_details[cam_mxid]["data"]:
                        combined_details[cam_mxid]["data"][date] = {}

                    if hour not in combined_details[cam_mxid]["data"][date]:
                        combined_details[cam_mxid]["data"][date][hour] = {"incoming": 0, "outgoing": 0}

                    combined_details[cam_mxid]["data"][date][hour]["incoming"] += entry["incoming"]
                    combined_details[cam_mxid]["data"][date][hour]["outgoing"] += entry["outgoing"]

        response_data = []

        for cam_mxid, details in combined_details.items():
            camera_info = {
                "MxID": cam_mxid,
                "details": {
                    "located": camera_objects.filter(MxID=cam_mxid).first().located,
                    "status": camera_objects.filter(MxID=cam_mxid).first().status,
                    "stream_link": camera_objects.filter(MxID=cam_mxid).first().stream_link,
                    "created_at": camera_objects.filter(MxID=cam_mxid).first().created_at,
                },
                "data": []
            }

            for date, hours_data in details["data"].items():
                for hour, counts in hours_data.items():
                    data_entry = {
                        "date": date,
                        "hour": hour,
                        "incoming": counts["incoming"],
                        "outgoing": counts["outgoing"],
                        "present": counts["incoming"] - counts["outgoing"],
                    }
                    camera_info["data"].append(data_entry)

            response_data.append(camera_info)

        return Response(response_data)













def get_token(username, password):
        API_URL = env("API_URL")
        global jwt_access_token
        token_endpoint = f'{API_URL}auth/token/'
        data = {
            'username': username,
            'password': password,
        }
        try:
            response = requests.post(token_endpoint, data=data)
            if response.status_code == 200:
                jwt_access_token = response.json().get('access')
                print("Token got successfully.")
            else:
                print(f"Token get failed with status code {response.status_code}")
        except Exception as e:
            print(f"Error getting token: {e}")