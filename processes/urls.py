from django.urls import path

from processes.views import index
from processes.views import process_list


urlpatterns = [
    path("", index, name="index"),
    path("processes/", process_list, name="process_list"),
]

app_name = "processes"

