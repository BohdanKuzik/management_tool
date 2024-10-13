import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect, render
import psutil
import logging

from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import ContextMixin

from processes.forms import RegisterUserForm
from processes.models import Snapshot

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'processes/process_list.html')


def get_processes(pid_filter=None, status_filter=None, name_filter=None):
    processes = []
    for proc in psutil.process_iter(["pid", "status", "name"]):
        try:

            if proc.pid == 0:
                continue

            if (pid_filter and str(proc.pid) != pid_filter) or \
               (status_filter and proc.status() != status_filter) or \
               (name_filter and name_filter.lower() not in proc.name().lower()):
                continue

            processes.append({
                "pid": proc.pid,
                "status": proc.status(),
                "start_time": timezone.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                "name": proc.name(),
                "memory_usage": round(proc.memory_info().rss / (1024 * 1024), 4),
                "cpu_usage": proc.cpu_percent(interval=0),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.warning(f"Error while accessing process: {e}")
    return processes


class ProcessListMixin(ContextMixin, View):
    def get_filtered_processes(self):
        pid_filter = self.request.GET.get("pid")
        status_filter = self.request.GET.get("status")
        name_filter = self.request.GET.get("name")

        processes = get_processes(pid_filter, status_filter, name_filter)
        return processes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["processes"] = self.get_filtered_processes()
        return context


class ProcessListView(ProcessListMixin, TemplateView):
    template_name = "processes/process_list.html"


class ProcessListPartialView(ProcessListMixin, TemplateView):
    template_name = "processes/process_table.html"


class KillProcessView(View):
    def post(self, request, pid, *args, **kwargs):
        try:
            p = psutil.Process(pid)
            p.terminate()
        except psutil.NoSuchProcess:
            logger.warning(f"Process {pid} not found.")
        except psutil.AccessDenied:
            logger.error(f"Access denied when trying to terminate process {pid}.")
        return redirect("processes:process_list")


def take_snapshot(request):
    if request.method == "POST":
        processes = get_processes()
        snapshot_data = json.dumps(processes)

        Snapshot.objects.create(
            author=request.user,
            process_data=snapshot_data,
            timestamp=timezone.now()
        )

        return redirect("processes:process_list")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "processes/register.html"
    success_url = reverse_lazy("processes:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign up"
        return context


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "processes/login.html"
    success_url = reverse_lazy("processes:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context
