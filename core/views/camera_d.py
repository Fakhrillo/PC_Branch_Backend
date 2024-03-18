from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
                "located": camera_objects.filter(MxID=cam_mxid).first().located,
                "status": camera_objects.filter(MxID=cam_mxid).first().status,
                "stream_link": camera_objects.filter(MxID=cam_mxid).first().stream_link,
                "created_at": camera_objects.filter(MxID=cam_mxid).first().created_at,
                "incoming": details["incoming"],
                "outgoing": details["outgoing"],
                "start_date": start_date_str if start_date_str else "N/A",
                "end_date": end_date_str if end_date_str else "N/A",
            })

        return Response(response_data)


class CameraWith24HoursData(APIView):
    permission_classes = [IsAdminUser, IsSuperUser]
    authentication_classes = [JWTAuthentication]

    jwt_access_token = None

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        camera_id = request.query_params.get('mxid')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            num_days = (end_date - start_date).days
            dates_str = {f"{hour:02d}:00": {"incoming": 0, "outgoing": 0, "present": 0} for hour in range(24)}
        else:
            current_hour = datetime.now().hour
            dates_str = {f"{hour:02d}:00": {"incoming": 0, "outgoing": 0, "present": 0} for hour in range(current_hour+1)}

        camera_objects = Camera_details.objects.filter(MxID=camera_id) if camera_id else Camera_details.objects.all()

        username = env("USERNAME")
        password = env("PASSWORD")
        API_URL = env("API_URL")
        
        get_token(username, password)
        headers = {'Authorization': f'Bearer {jwt_access_token}'}

        combined_data = defaultdict(lambda: {"incoming": 0, "outgoing": 0})
        data = []

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
                    hour = created_at.strftime("%H:00")
                    combined_data[hour]["incoming"] += entry["incoming"]
                    combined_data[hour]["outgoing"] += entry["outgoing"]
                    
        total_in = total_out = 0
        for hour, counts in sorted(combined_data.items()):
            total_in += counts["incoming"]
            total_out += counts["outgoing"]
            present = total_in - total_out

            dates_str[hour]["incoming"] = counts["incoming"]
            dates_str[hour]["outgoing"] = counts["outgoing"]
            dates_str[hour]["present"] = present if present >= 0 else 0

        for hour, counts in dates_str.items():
            data.append({
                "hour": hour,
                "incoming": counts["incoming"],
                "outgoing": counts["outgoing"],
                "present": counts["present"]
            })

        return Response({"data": data})


class CameraDetailsForMobile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    jwt_access_token = None

    def get(self, request, *args, **kwargs):

        camera_objects = Camera_details.objects.all()

        username = env("USERNAME")
        password = env("PASSWORD")
        API_URL = env("API_URL")
        
        get_token(username, password)
        headers = {'Authorization': f'Bearer {jwt_access_token}'}

        combined_data = defaultdict(lambda: {"incoming": 0, "outgoing": 0})

        for camera_object in camera_objects:
            cam_mxid = camera_object.MxID
            url = f"{API_URL}camera/tracked/{cam_mxid}"

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                count_details = response.json()

                for entry in count_details:
                    created_at = datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    hour = created_at.strftime("%Y-%m-%d %H:00")
                    combined_data[hour]["incoming"] += entry["incoming"]
                    combined_data[hour]["outgoing"] += entry["outgoing"]

        response_data = {"total_counts": [], "data":[]}
        total_counts = {"total_incoming": 0, "total_outgoing": 0, "total_present": 0}

        for hour, counts in reversed(combined_data.items()):
            total_counts["total_incoming"] += counts["incoming"]
            total_counts["total_outgoing"] += counts["outgoing"]
            total_counts["total_present"] += counts["incoming"] - counts["outgoing"]
            data_entry = {
                "hour": hour,
                "incoming": counts["incoming"],
                "outgoing": counts["outgoing"],
                "present": counts["incoming"] - counts["outgoing"],
            }
            response_data["data"].append(data_entry)

        response_data["total_counts"].append(total_counts)

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