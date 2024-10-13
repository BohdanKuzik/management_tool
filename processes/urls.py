from django.urls import path

from processes.views import (
    index,
    ProcessListView,
    ProcessListPartialView,
    KillProcessView,
    take_snapshot,
    RegisterUser,
    LoginUser,
    logout_user,
    SnapshotListView,
    snapshot_details,
)


urlpatterns = [
    path("", index, name="index"),
    path("processes/", ProcessListView.as_view(), name="process_list"),
    path("processes/partial/", ProcessListPartialView.as_view(), name="process_list_partial"),
    path("processes/kill/<int:pid>/", KillProcessView.as_view(), name="kill_process"),
    path("processes/take_snapshot/", take_snapshot, name="take_snapshot"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("snapshots/", SnapshotListView.as_view(), name="snapshot_list"),
    path("snapshots/<int:pk>/", snapshot_details, name="snapshot_detail"),
]

app_name = "processes"

