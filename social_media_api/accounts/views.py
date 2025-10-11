from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'template/relationship_app/register.html'



class LogInView():
    def my_login_view(request):
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # start session
                return redirect("member")
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        return render(request, "login.html")


class LogOutView():
    def my_logout_view(request):
        logout(request)
        return redirect("login")
    

