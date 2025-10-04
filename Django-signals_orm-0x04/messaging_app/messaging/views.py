from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    Allow the logged-in user to delete their account.
    """
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({"message": f"User {username} and all related data have been deleted."})
