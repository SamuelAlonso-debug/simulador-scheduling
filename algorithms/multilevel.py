from algorithms.fcfs import fcfs
from algorithms.round_robin import round_robin
from algorithms.sjf import sjf


def multilevel_queue_scheduler(processes, queues_config):
    time = 0
    gantt = []
    queue_history = [] 

    queues = {level: [] for level in queues_config}

    processes = sorted(processes, key=lambda p: p.arrival_time)
    pending = processes.copy()

    while pending or any(queues.values()):

        # Agregar procesos que ya llegaron
        for p in pending[:]:
            if p.arrival_time <= time:
                queues[p.queue_level].append(p)
                pending.remove(p)

        # GUARDAR ESTADO DE COLAS
        snapshot = {
            level: [p.pid for p in queues[level]]
            for level in queues
        }
        queue_history.append((time, snapshot))

        executed = False

        for level in sorted(queues.keys()):
            queue = queues[level]

            if queue:
                config = queues_config[level]

                if config["type"] == "fcfs":
                    entry, new_time = fcfs(queue, time)

                elif config["type"] == "rr":
                    entry, new_time = round_robin(
                        queue,
                        config["quantum"],
                        time
                    )

                elif config["type"] == "sjf":
                    entry, new_time = sjf(queue, time)

                else:
                    raise ValueError("Algoritmo no soportado")

                if entry:
                    gantt.append(entry)
                    time = new_time
                    executed = True
                    break

        if not executed:
            time += 1

    return gantt, queue_history 