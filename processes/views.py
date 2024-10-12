import psutil
import logging
from django.utils import timezone
from django.shortcuts import render


logger = logging.getLogger(__name__)


def index(request):
    num_four = 2 + 2

    context = {
        "num_four": num_four,
    }

    return render(request, "processes/index.html", context=context)


def get_processes():
    processes = []
    for proc in psutil.process_iter(["pid", "status", "name"]):
        try:
            processes.append({
                "pid": proc.pid,
                "status": proc.status(),
                "start_time": timezone.datetime.fromtimestamp(proc.create_time()),
                "name": proc.name(),
                "memory_usage": proc.memory_info().rss / (1024 * 1024),
                "cpu_usage": proc.cpu_percent(interval=0),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.warning(f"Error while accessing process: {e}")
    return processes


def process_list(request):
    processes = get_processes()
    return render(request, "processes/process_list.html", {"processes": processes})


def process_list_partial(request):
    processes = get_processes()
    return render(request, "processes/process_table.html", {"processes": processes})
