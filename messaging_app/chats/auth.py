from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# These can be imported in urls.py directly if you prefer,
# but having them here keeps all auth logic in chats app
__all__ = ["TokenObtainPairView", "TokenRefreshView"]
