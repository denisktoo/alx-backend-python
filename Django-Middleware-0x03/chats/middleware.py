from datetime import datetime
from django.http import HttpResponseForbidden
import os

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_path = os.path.join(os.path.dirname(__file__), "requests.log")

    def __call__(self, request):
        with open(self.log_path, "a") as log_file:
            user = request.user
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)

        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access denied: only allowed between 6PM and 9PM.")

        return self.get_response(request)
