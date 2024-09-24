import logging
from logging import FileHandler  # FileHandler is in logging, not logging.handlers
import json
import os
from django.utils.timezone import now
from django.conf import settings

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Create the directory if it doesn't exist
        self.log_dir = os.path.join(settings.BASE_DIR, 'logs', 'user_activity')
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up the logger for file-based logging
        self.logger = logging.getLogger('user_activity')

        # Define the log file path
        log_file_path = os.path.join(self.log_dir, 'user_activity.log')

        # Configure the file handler (set limit to 200MB, no backup or deletion)
        handler = FileHandler(log_file_path)  # Fixed import here
        formatter = logging.Formatter('%(message)s')  # Simple format for JSON entries
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Set a limit of 200MB and handle file manually
        self.max_size_bytes = 200 * 1024 * 1024  # 200 MB

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Log user activity after the response
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.log_user_activity(request)

        return response

    def log_user_activity(self, request):
        user = request.user.username
        path = request.path
        time_visited = now().isoformat()  # Use ISO format for timestamps

        # Create a log entry in JSON format for easy parsing
        log_entry = {
            "user": user,
            "path": path,
            "time_visited": time_visited
        }

        # Ensure log file does not exceed 200 MB
        self._check_log_size()

        # Log the data as a JSON string
        self.logger.info(json.dumps(log_entry))

    def _check_log_size(self):
        log_file_path = os.path.join(self.log_dir, 'user_activity.log')
        if os.path.exists(log_file_path):
            current_size = os.path.getsize(log_file_path)
            if current_size > self.max_size_bytes:
                # Move the current log file to another name to preserve it
                new_log_file_path = log_file_path.replace('.log', f'_{now().strftime("%Y%m%d_%H%M%S")}.log')
                os.rename(log_file_path, new_log_file_path)

                # Reset the logger to write to a new file
                self.logger.handlers = []  # Clear existing handlers
                handler = FileHandler(log_file_path)
                handler.setFormatter(logging.Formatter('%(message)s'))
                self.logger.addHandler(handler)
