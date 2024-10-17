import json
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    redirect,
    get_object_or_404,
    render,
)
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from processes.models import Snapshot
from processes.managers import SnapshotManager, ProcessManager


@login_required
def take_snapshot(request) -> Any:
    if request.method == "POST":
        try:
            processes = ProcessManager.get_processes()
            SnapshotManager.create_snapshot(request.user, processes)
            messages.success(request, "Snapshot successfully created!")
        except Exception as e:
            messages.error(request, str(e))

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
