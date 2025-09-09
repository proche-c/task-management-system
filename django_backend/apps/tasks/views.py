from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import requests
from apps.tasks.models import Task

class TaskListView(View):  
    template_name = "tasks_list.html"

    def get(self, request):
        # using ORM
        if request.user.is_authenticated:
            tasks = Task.objects.select_related('created_by', 'parent_task').prefetch_related('assigned_to', 'tags').all()
            return render(request, self.template_name, {"tasks": tasks})

        # if useer is not authenticated in Django, use API with JWT
        access = request.session.get("access_token")
        if access:
            api_url = f"{request.scheme}://{request.get_host()}/api/tasks/"
            try:
                resp = requests.get(api_url, headers={"Authorization": f"Bearer {access}"}, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    tasks_json = data.get("results", data) 
                    return render(request, self.template_name, {"tasks_json": tasks_json})
                else:
                    request.session.pop("access_token", None)
                    return redirect("login")
            except requests.RequestException:
                return render(request, self.template_name, {"error": "Could not fetch tasks from API."})

        return redirect("login")
    
class NewTaskView(LoginRequiredMixin, View):
    template_name = "new_task.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")
        estimated_hours = request.POST.get("estimated_hours") or 0

        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
            created_by=request.user
        )

        messages.success(request, "Task created successfully!")
        return redirect("tasks_list")  


# class NewTaskView(View):
#     template_name = "new_task.html"

#     def get(self, request):
#         tasks = Task.objects.select_related("created_by").prefetch_related("assigned_to")
#         return render(request, self.template_name, {"tasks": tasks})

#     def post(self, request):
#         # Capturamos los datos del formulario
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         status = request.POST.get("status")
#         priority = request.POST.get("priority")
#         due_date = request.POST.get("due_date")
#         estimated_hours = request.POST.get("estimated_hours")

#         # Endpoint de la API
#         api_url = "http://localhost:8000/api/tasks/"

#         # Data que enviaremos al endpoint
#         payload = {
#             "title": title,
#             "description": description,
#             "status": status,
#             "priority": priority,
#             "due_date": due_date,
#             "estimated_hours": estimated_hours
#         }

#         # Hacer POST usando la cookie de sesión para autenticación
#         session = requests.Session()
#         for key, value in request.COOKIES.items():
#             session.cookies.set(key, value)

#         response = session.post(api_url, json=payload)

#         if response.status_code in (200, 201):
#             # Task creada correctamente
#             return render(request, self.template_name, {"success": "Task created successfully"})
#         else:
#             # Error al crear
#             error_msg = response.json().get("detail") or "Failed to create task"
#             return render(request, self.template_name, {"error": error_msg})

class TaskDetailView(LoginRequiredMixin, View):
    template_name = "task_detail.html"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, self.template_name, {"task": task})