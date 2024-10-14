import logging
from typing import Any, Dict

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from processes.forms import RegisterUserForm

logger = logging.getLogger(__name__)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "processes/register.html"
    success_url = reverse_lazy("processes:login")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign up"
        return context


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "processes/login.html"
    success_url = reverse_lazy("processes:login")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context


def logout_user(request) -> Any:
    logout(request)
    return redirect("processes:login")
