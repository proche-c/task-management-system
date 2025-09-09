from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
import requests

class UserLoginView(View):
    """
    View to handle user login.

    GET:
        - Renders the login page ('login.html') with the login form.

    POST:
        - Retrieves the username and password from the submitted form.
        - Sends a POST request to the API token endpoint to authenticate the user.
        - If authentication is successful:
            - Stores the access token in the session.
            - Redirects the user to the tasks page.
        - If authentication fails:
            - Re-renders the login page with an error message.
    """
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
            request.session["access_token"] = access_token 
            return redirect("/tasks/")

        return render(request, self.template_name, {"error": "Credenciales inválidas"})
    
class UserLogoutView(View):
    """
    View to handle user logout.

    POST:
        - Logs out the current user.
        - Redirects to the login page.
    """
    def post(self, request):
        logout(request)
        return redirect('/login/') 

