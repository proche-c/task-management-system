from rest_framework.routers import DefaultRouter
from apps.tasks.api.views import TaskViewSet

router_tasks = DefaultRouter()
router_tasks.register(prefix='tasks', basename='tasks', viewset=TaskViewSet)