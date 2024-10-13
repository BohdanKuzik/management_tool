from django.urls import path

from processes.views import (
    index,
    ProcessListView,
    ProcessListPartialView,
    KillProcessView,
    take_snapshot,
    RegisterUser,
    LoginUser,
)


urlpatterns = [
    path("", index, name="index"),
    path("processes/", ProcessListView.as_view(), name="process_list"),
    path("processes/partial/", ProcessListPartialView.as_view(), name="process_list_partial"),
    path("processes/kill/<int:pid>/", KillProcessView.as_view(), name="kill_process"),
    path("processes/take_snapshot/", take_snapshot, name="take_snapshot"),
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register")
]

app_name = "processes"

