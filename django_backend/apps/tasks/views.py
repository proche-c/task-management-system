from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

class TaskListView(LoginRequiredMixin, View):
    template_name = "tasks_list.html"  # ruta a tu template

    def get(self, request):
        # No necesitamos pasar las tareas desde aquí, el JS del template hará fetch a la API
        return render(request, self.template_name)


class NewTaskView(View):
    template_name = "new_task.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Capturamos los datos del formulario
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")
        estimated_hours = request.POST.get("estimated_hours")

        # Endpoint de la API
        api_url = "http://localhost:8000/api/tasks/"

        # Data que enviaremos al endpoint
        payload = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "estimated_hours": estimated_hours
        }

        # Hacer POST usando la cookie de sesión para autenticación
        session = requests.Session()
        for key, value in request.COOKIES.items():
            session.cookies.set(key, value)

        response = session.post(api_url, json=payload)

        if response.status_code in (200, 201):
            # Task creada correctamente
            return render(request, self.template_name, {"success": "Task created successfully"})
        else:
            # Error al crear
            error_msg = response.json().get("detail") or "Failed to create task"
            return render(request, self.template_name, {"error": error_msg})

class TaskDetailView(View):
    template_name = "task_detail.html"

    def get(self, request, task_id):
        return render(request, self.template_name, {"task_id": task_id})