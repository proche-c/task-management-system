from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
import requests

class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        api_url = "http://localhost:8000/api/auth/token/"
        response = requests.post(api_url, data={"username": username, "password": password})

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            request.session["access_token"] = access_token  # guardarlo en sesión
            return redirect("/tasks/")

        return render(request, self.template_name, {"error": "Credenciales inválidas"})
    
class UserLogoutView(View):
    def post(self, request):
        logout(request)  # elimina la sesión
        return redirect('/login/')  # redirige al login

