def calculate_metrics(processes, gantt):
    completion_time = {}
    turnaround_time = {}
    waiting_time = {}

    # Obtener tiempo de finalización
    for entry in gantt:
        completion_time[entry.pid] = entry.end

    for p in processes:
        ct = completion_time[p.pid]
        tat = ct - p.arrival_time
        wt = tat - p.burst_time

        turnaround_time[p.pid] = tat
        waiting_time[p.pid] = wt

    # PROMEDIOS
    n = len(processes)

    avg_tat = sum(turnaround_time.values()) / n
    avg_wt = sum(waiting_time.values()) / n

    return {
        "completion_time": completion_time,
        "turnaround_time": turnaround_time,
        "waiting_time": waiting_time,
        "avg_turnaround": avg_tat,
        "avg_waiting": avg_wt
    }