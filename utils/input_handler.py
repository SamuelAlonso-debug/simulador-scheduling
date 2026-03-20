def get_processes_from_user():
    processes = []

    n = int(input("¿Cuántos procesos deseas ingresar?: "))

    for i in range(n):
        print(f"\nProceso {i+1}")

        pid = input("PID: ")
        arrival = int(input("Tiempo de llegada: "))
        burst = int(input("Burst time: "))
        queue = int(input("Nivel de cola (0 = mayor prioridad): "))

        processes.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "queue": queue
        })

    return processes


def get_queue_config():
    config = {}

    levels = int(input("\n¿Cuántas colas quieres?: "))

    for i in range(levels):
        print(f"\nConfiguración cola {i}")

        algo = input("Algoritmo (fcfs / rr / sjf): ").lower()

        if algo == "rr":
            quantum = int(input("Quantum: "))
            config[i] = {"type": "rr", "quantum": quantum}
        else:
            config[i] = {"type": "fcfs"}

    return config