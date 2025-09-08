"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.api.router import router_auth, router_users
from apps.tasks.api.router import router_tasks
from apps.users.views import UserLoginView, UserLogoutView
from apps.tasks.views import TaskListView, NewTaskView, TaskDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_auth.urls)),
    path('api/', include(router_users.urls)),
    path('api/', include(router_tasks.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('tasks/', TaskListView.as_view(), name='tasks_list'),
    path('new_task/', NewTaskView.as_view(), name='new_task'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail')
]
