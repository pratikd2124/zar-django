from django.utils.timezone import now
class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request after the user is attached to the request
        response = self.get_response(request)

        # Log user activity after the response
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.log_user_activity(request)

        return response

    def log_user_activity(self, request):
        user = request.user
        path = request.path
        time_visited = now()

        # Log to the database (or wherever you want to store this information)
        from .models import UserActivity
        UserActivity.objects.create(user=user, page_visited=path, timestamp=time_visited)
