from django.urls import path

from processes.views import index
from processes.views import (
    process_list,
    process_list_partial,
    kill_process,
)


urlpatterns = [
    path("", index, name="index"),
    path("processes/", process_list, name="process_list"),
    path('processes/partial/', process_list_partial, name='process_list_partial'),
    path('processes/kill/<int:pid>/', kill_process, name='kill_process'),
]

app_name = "processes"

