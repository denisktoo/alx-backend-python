from datetime import datetime
import time
from django.http import HttpResponseForbidden
import os

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Authorization Header:", request.META.get('HTTP_AUTHORIZATION'))
        print("User:", request.user)
        response = self.get_response(request)
        return response

# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#         base_dir = os.path.dirname(os.path.dirname(__file__))
#         self.log_path = os.path.join(base_dir, "requests.log")

#     def __call__(self, request):
#         with open(self.log_path, "a") as log_file:
#             user = request.user
#             log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}")

#         response = self.get_response(request)

#         return response

# class RestrictAccessByTimeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         current_hour = datetime.now().hour

#         if current_hour < 18 or current_hour >= 21:
#             return HttpResponseForbidden("Access denied: only allowed between 6PM and 9PM.")

#         return self.get_response(request)
    
# class OffensiveLanguageMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # Store timestamps of POSTs per IP
#         self.message_logs = {}

#     def __call__(self, request):
#         # Get the client's IP address, accounting for proxy headers.
#         if request.method == 'POST':
#             ip_address = self.get_client_ip(request)
#             now = time.time()
            
#             # Initialize list for new IP
#             if ip_address not in self.message_logs:
#                 self.message_logs[ip_address] = []

#             # Keep only timestamps within the last 60 seconds
#             one_minute_ago = now - 60
#             self.message_logs[ip_address] = [
#                 timestamp for timestamp in self.message_logs[ip_address]
#                 if timestamp > one_minute_ago
#             ]

#             # Check if limit exceeded
#             if len(self.message_logs[ip_address]) >= 5:
#                 return HttpResponseForbidden("Too many messages sent. Try again later.")

#             # Log current message timestamp
#             self.message_logs[ip_address].append(now)

#         # Continue processing request
#         return self.get_response(request)

#     def get_client_ip(self, request):
#         """Get the client's IP address, accounting for proxy headers."""
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             return x_forwarded_for.split(',')[0].strip()
#         return request.META.get('REMOTE_ADDR')

# class RolepermissionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Allow unauthenticated access to token and registration endpoints
#         if request.path in ['/api/token/', '/api/register/', '/api/users/']:
#             return self.get_response(request)
        
#         user = request.user

#         # Check if user is authenticated and has a valid role
#         if user.is_authenticated:
#             # Only allow 'admin' or 'host' roles
#             if getattr(user, 'role', None) not in ['admin', 'host']:
#                 return HttpResponseForbidden("Access denied: Admins or Hosts only")
#         else:
#             return HttpResponseForbidden("Access denied: Login required")

#         return self.get_response(request)
