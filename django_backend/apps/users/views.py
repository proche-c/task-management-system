from django.shortcuts import render, redirect
from django.views import View
import requests

class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        api_url = "http://localhost:8000/api/auth/login/"
        response = requests.post(api_url, data={"username": username, "password": password})

        if response.status_code == 200:
            # # Aquí podrías guardar el token JWT o la cookie en la sesión de Django
            # request.session["auth_token"] = response.json().get("token")
            return render(request, self.template_name, {"success": "Login successful"})

        # Si falla, recargar el form con error
        return render(request, self.template_name, {"error": "Credenciales inválidas"})

