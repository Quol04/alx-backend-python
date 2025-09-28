import logging
from datetime import datetime
from django.http import HttpResponseForbidden

import time
from collections import defaultdict, deque


# Configure logger for writing into requests.log
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """Called once when the server starts"""
        self.get_response = get_response

    def __call__(self, request):
        """Called on each request"""
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response



# ----------=====================================

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """Called once when the server starts"""
        self.get_response = get_response

    def __call__(self, request):
        """Check server time before processing request"""
        now = datetime.now().time()
        start_time = datetime.strptime("06:00", "%H:%M").time()  # 6 AM
        end_time = datetime.strptime("21:00", "%H:%M").time()    # 9 PM

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access to the chat app is restricted outside 6AM - 9PM.</p>"
            )

        response = self.get_response(request)
        return response


# =----------=====================================



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware"""
        self.get_response = get_response
        # Track messages per IP: { ip: deque([timestamps]) }
        self.message_log = defaultdict(lambda: deque())

        # Configurable values
        self.limit = 5            # messages allowed
        self.time_window = 60     # seconds (1 minute)

    def __call__(self, request):
        # Only check POST requests to chat endpoints
        if request.method == "POST" and "/chats/" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Get request history for this IP
            timestamps = self.message_log[ip]

            # Remove old requests outside the time window
            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            if len(timestamps) >= self.limit:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Message limit exceeded. "
                    "You can only send 5 messages per minute.</p>"
                )

            # Add current timestamp
            timestamps.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# =----------=====================================



class RolepermissionMiddleware:
    def __init__(self, get_response):
        """Called once at server startup"""
        self.get_response = get_response

    def __call__(self, request):
        """
        Called for each request.
        Deny access if user is not 'admin' or 'moderator'.
        """
        user = request.user

        # Only check authenticated users
        if user.is_authenticated:
            # Example: assume user model has a "role" field
            role = getattr(user, "role", None)

            if role not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You do not have permission to access this resource.</p>"
                )

        response = self.get_response(request)
        return response
