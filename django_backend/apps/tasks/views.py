from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import requests
from apps.tasks.models import Task

class TaskListView(View):
    """
    View to display the list of tasks.

    - If the user is authenticated in Django:
        - Retrieves tasks using the ORM with `select_related` and `prefetch_related`.
        - Renders 'tasks_list.html' with the retrieved tasks.

    - If the user is not authenticated in Django but has a JWT in session:
        - Makes a request to the internal task API using the access token.
        - Renders 'tasks_list.html' with the tasks data from the API.

    - If no valid user or token is present:
        - Redirects to the login page.
    """
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
    """
    View to create a new task.

    GET:
        - Renders 'new_task.html' template with a task creation form.

    POST:
        - Collects task data from the submitted form.
        - Creates a new Task object in the database.
        - Displays a success message.
        - Redirects to the task list page.
    """
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


class TaskDetailView(LoginRequiredMixin, View):
    """
    View to display the details of a single task.

    GET:
        - Fetches the task by ID using `get_object_or_404`.
        - Renders 'task_detail.html' template with the task data.
    """
    template_name = "task_detail.html"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, self.template_name, {"task": task})