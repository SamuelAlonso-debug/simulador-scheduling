from models.process import Process
from core.scheduler import run_scheduler
from utils.metrics import calculate_metrics
from utils.input_handler import get_processes_from_user, get_queue_config


def main():
    raw_processes = get_processes_from_user()
    config = get_queue_config()

    processes = []
    
    for p in raw_processes:
        processes.append(
            Process(
                pid=p["pid"],
                arrival_time=p["arrival"],
                burst_time=p["burst"],
                remaining_time=p["burst"],
                queue_level=p["queue"]
            )
        )

    gantt = run_scheduler(processes, config)

    print("\n=== Gantt ===")
    for g in gantt:
        print(f"{g.pid}: {g.start} -> {g.end}")

    metrics = calculate_metrics(processes, gantt)

    print("\n=== Métricas ===")
    print("Turnaround:", metrics["turnaround_time"])
    print("Waiting:", metrics["waiting_time"])


if __name__ == "__main__":
    main()