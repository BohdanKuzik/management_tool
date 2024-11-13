from typing import (
    Any,
    Dict,
    List,
)

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.base import View

from processes.managers import ProcessManager


class ProcessListMixin(TemplateView):
    def get_filtered_processes(self) -> List[Dict[str, Any]]:
        pid_filter = self.request.GET.get("pid")
        status_filter = self.request.GET.get("status")
        name_filter = self.request.GET.get("name")

        processes = ProcessManager.get_processes(
            pid_filter,
            status_filter,
            name_filter
        )
        return processes

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["processes"] = self.get_filtered_processes()
        return context


class ProcessListView(LoginRequiredMixin, ProcessListMixin):
    template_name = "processes/process_list.html"


class ProcessListPartialView(
    LoginRequiredMixin,
    ProcessListMixin
):
    template_name = "processes/process_table.html"


class KillProcessView(View):
    def post(self, request, pid, *args, **kwargs) -> Any:
        try:
            ProcessManager.kill_process(pid)
            messages.success(
                request,
                f"Process {pid} successfully terminated."
            )
        except Exception as e:
            messages.error(request, str(e))
        return redirect("processes:process_list")
