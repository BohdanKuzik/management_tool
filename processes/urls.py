from django.urls import path

from processes.views import index
from processes.views import process_list, process_list_partial


urlpatterns = [
    path("", index, name="index"),
    path("processes/", process_list, name="process_list"),
    path('processes/partial/', process_list_partial, name='process_list_partial'),
]

app_name = "processes"

