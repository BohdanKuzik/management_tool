import json
import logging
from typing import (
    Any,
    Dict,
    List,
)

import psutil
from django.utils import timezone

from processes.models import Snapshot

logger = logging.getLogger(__name__)


class ProcessManager:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
                if not ProcessManager.filter_processes(
                        proc,
                        pid_filter,
                        status_filter,
                        name_filter
                ):
                    continue
                processes.append(ProcessManager.format_process_data(proc))
            except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess
            ) as e:
                logger.warning(f"Error while accessing process: {e}")
        return processes

    @staticmethod
    def kill_process(pid: int):
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            logger.warning(f"Process {pid} not found.")
            raise Exception("Process not found.")
        except psutil.AccessDenied:
            logger.error(
                f"Access denied when trying to terminate process {pid}."
            )
            raise Exception("Access denied.")


class SnapshotManager:
    @staticmethod
    def create_snapshot(user, processes):
        try:
            snapshot_data = json.dumps(processes)
            Snapshot.objects.create(
                author=user,
                process_data=snapshot_data,
                timestamp=timezone.now(),
            )
        except Exception as e:
            raise Exception(f"Error while creating snapshot: {str(e)}")
