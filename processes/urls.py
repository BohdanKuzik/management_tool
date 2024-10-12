from django.urls import path

from processes.views import (
    index,
    ProcessListView,
    ProcessListPartialView,
    KillProcessView,
    take_snapshot,
)


urlpatterns = [
    path("", index, name="index"),
    path("processes/", ProcessListView.as_view(), name="process_list"),
    path("processes/partial/", ProcessListPartialView.as_view(), name="process_list_partial"),
    path("processes/kill/<int:pid>/", KillProcessView.as_view(), name="kill_process"),
    path("processes/take_snapshot/", take_snapshot, name="take_snapshot"),
]

app_name = "processes"

