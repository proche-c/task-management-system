from rest_framework.routers import DefaultRouter
from apps.users.api.views import AuthViewSet, UserViewSet

router_auth = DefaultRouter()
router_auth.register(prefix='auth', basename='auth', viewset=AuthViewSet)

router_users = DefaultRouter()
router_users.register(prefix='users', basename='users', viewset=UserViewSet)