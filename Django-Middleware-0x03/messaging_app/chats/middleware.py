import 

class RequestLoggingMiddleware:
    def __init__(self, get_reslonse):
        self.get_response = get_response

    def __call__(request):
        with open("requests.log, "a") as log_file:
        log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}“)

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
