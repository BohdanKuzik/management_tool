import json
import logging

from typing import (
    Any,
    Dict,
    List,
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
)
from django.views.generic.base import ContextMixin

import psutil

from processes.models import Snapshot

logger = logging.getLogger(__name__)


@login_required
def index(request) -> Any:
    return render(request, "processes/process_list.html")


def filter_processes(
        proc,
        pid_filter=None,
        status_filter=None,
        name_filter=None
) -> bool:
    if pid_filter and str(proc.pid) != pid_filter:
        return False
    if status_filter and proc.status() != status_filter:
        return False
    if name_filter and name_filter.lower() not in proc.name().lower():
        return False
    return True


def format_process_data(proc) -> Dict[str, Any]:
    return {
        "pid": proc.pid,
        "status": proc.status(),
        "start_time": timezone.datetime.fromtimestamp(
            proc.create_time()
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "name": proc.name(),
        "memory_usage": round(
            proc.memory_info().rss / (1024 * 1024), 4
        ),
        "cpu_usage": proc.cpu_percent(interval=0),
    }


def get_processes(
        pid_filter=None,
        status_filter=None,
        name_filter=None
) -> List[Dict[str, Any]]:
    processes = []

    for proc in psutil.process_iter(["pid", "status", "name"]):
        try:
            if proc.pid == 0:
                continue

            if not filter_processes(
                    proc,
                    pid_filter,
                    status_filter,
                    name_filter
            ):
                continue

            processes.append(format_process_data(proc))
        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
        ) as e:
            logger.warning(f"Error while accessing process: {e}")
    return processes


class ProcessListMixin(ContextMixin, View):
    def get_filtered_processes(self) -> List[Dict[str, Any]]:
        pid_filter = self.request.GET.get("pid")
        status_filter = self.request.GET.get("status")
        name_filter = self.request.GET.get("name")

        processes = get_processes(pid_filter, status_filter, name_filter)
        return processes

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["processes"] = self.get_filtered_processes()
        return context


@method_decorator(login_required, name="dispatch")
class ProcessListView(ProcessListMixin, TemplateView):
    template_name = "processes/process_list.html"


class ProcessListPartialView(
    LoginRequiredMixin,
    ProcessListMixin,
    TemplateView
):
    template_name = "processes/process_table.html"


class KillProcessView(View):
    def post(self, request, pid, *args, **kwargs) -> Any:
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            logger.warning(f"Process {pid} not found.")
        except psutil.AccessDenied:
            logger.error(
                f"Access denied when trying to terminate process {pid}."
            )
        return redirect("processes:process_list")


@login_required
def take_snapshot(request) -> Any:
    if request.method == "POST":
        try:
            processes = get_processes()
            snapshot_data = json.dumps(processes)

            Snapshot.objects.create(
                author=request.user,
                process_data=snapshot_data,
                timestamp=timezone.now(),
            )
            messages.success(request, "Snapshot successfully created!")
        except Exception as e:
            messages.error(request, "Error while creating snapshot: " + str(e))

        return redirect("processes:process_list")


class SnapshotListView(LoginRequiredMixin, ListView):
    model = Snapshot
    template_name = "processes/snapshot_list.html"
    context_object_name = "snapshots"
    ordering = ["-timestamp"]


@login_required
def snapshot_details(request, pk) -> Any:
    snapshot = get_object_or_404(Snapshot, id=pk)
    process_data = json.loads(snapshot.process_data)

    context = {
        "snapshot": snapshot,
        "process_data": process_data,
    }

    return render(request, "processes/snapshot_detail.html", context)
