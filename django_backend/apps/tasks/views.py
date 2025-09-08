from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin, View):
    template_name = "tasks_list.html"  # ruta a tu template

    def get(self, request):
        # No necesitamos pasar las tareas desde aquí, el JS del template hará fetch a la API
        return render(request, self.template_name)


