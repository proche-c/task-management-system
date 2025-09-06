from rest_framework.routers import DefaultRouter
from apps.users.api.views import AuthViewSet

router_auth = DefaultRouter()
router_auth.register(prefix='auth', basename='auth', viewset=AuthViewSet)